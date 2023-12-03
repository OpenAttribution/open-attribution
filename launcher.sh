#!/bin/bash
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#
#  								#
#  options:							#
#  	--stop ALL services stopped: druid, kafka & API         #
#  	--status prints tail journal logs for services          #
#								#
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#

# Warning: set -e can make debugging tricky
#set -Ee
set -u
set -o pipefail
#set -x

if ! source ./local.conf; then
	echo "Error: Unable to source local.conf. Check you are in open-attribution directory. Copy with: cp example_local.conf local.conf"
	exit 1
fi

# Check if the script is being run as root
if [ "$EUID" -ne 0 ]; then
	echo "Please run as root"
	exit
fi

# Function to stop systemd services
stop_services() {
	echo "Stopping all managed systemd services..."
	systemctl stop open-attribution-api.service
	systemctl stop open-attribution-kafka.service
	systemctl stop open-attribution-druid.service
	systemctl stop clickhouse-server.service
	exit
}

# Function to echo systemd status
echo_status() {
	# Add command to display status here
	echo "++++++++++++++++++++++++"
	echo "Systemd services status:"
	echo "++++++++++++++++++++++++"
	echo ""
	echo "++++++++++++++++++++++++"
	echo "Systemd services status: clickhouse"
	echo "++++++++++++++++++++++++"
	systemctl status clickhouse-server.service
	#journalctl -u open-attribution-clickhouse.service | tail -n 10
	echo "++++++++++++++++++++++++"
	echo ""
	echo "++++++++++++++++++++++++"
	echo "Systemd services status: kafka"
	echo "++++++++++++++++++++++++"
	systemctl status open-attribution-kafka.service
	#journalctl -u open-attribution-kafka.service | tail -n 10
	echo "++++++++++++++++++++++++"
	echo ""
	echo "++++++++++++++++++++++++"
	echo "Systemd services status: python api"
	echo "++++++++++++++++++++++++"
	systemctl status open-attribution-api.service
	#journalctl -u open-attribution-api.service | tail -n 10
	echo "++++++++++++++++++++++++"
	exit
}

# Print and handle error
function __error_handing__() {
	local last_status_code=$1
	local error_line_number=$2
	echo 1>&2 "Error - exited with status $last_status_code at line $error_line_number"
	perl -slne 'if($.+5 >= $ln && $.-4 <= $ln){ $_="$. $_"; s/$ln/">" x length($ln)/eg; s/^\D+.*?$/\e[1;31m$&\e[0m/g;  print}' -- -ln="$error_line_number" "$0"
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
	case $1 in
	-s | --stop)
		stop_services
		;;
	-i | --status)
		echo_status
		;;
	*)
		echo "Unknown option: $1"
		exit 1
		;;
	esac
	#shift
done

trap '__error_handing__ $? $LINENO' ERR

source ./local.conf

app_dir=$(pwd)

# Check & create users: kafka
if ! id "kafka" &>/dev/null; then
	sudo useradd -r -s /bin/false kafka
	echo "User 'kafka' created."
fi

# Assemble ClickHouse systemd service file and starts it
function start-clickhouse {
	sudo service clickhouse-server start
}

# Assembles the Kafka systemd service file and starts it
function start-kafka {
	echo "Start kafka service"
	echo "kafka_dir: $KAFKA_DIR"
	setfacl -R -m u:kafka:rwx $KAFKA_DIR
	cat <<EOF >/etc/systemd/system/open-attribution-kafka.service
[Unit]
Description=Open Attribution Kafka service
After=network.target

[Service]
User=kafka
Group=kafka
ExecStart=${KAFKA_DIR}/bin/kafka-server-start.sh ${KAFKA_DIR}/config/server.properties  --override advertised.listeners=PLAINTEXT://localhost:9092 --override listeners=PLAINTEXT://localhost:9092
ExecReload=/bin/kill -s HUP \$MAINPID
Restart=on-failure
KillMode=mixed
PrivateTmp=true

[Install]
WantedBy=multi-user.target

EOF
	systemctl daemon-reload
	systemctl start open-attribution-kafka.service
}

# Assemble Python litestar api systemd service file and starts it
#Environment="PATH=${PYTHON_ENV_DIR}/bin:$PATH"
function start-api {
	echo "Start python api service"
	cat <<EOF >/etc/systemd/system/open-attribution-api.service
[Unit]
Description=Gunicorn instance to serve Open Attribution API
After=network.target

[Service]
RuntimeDirectory=gunicorn-api
WorkingDirectory=${app_dir}
ExecStart=${PYTHON_ENV_DIR}/bin/gunicorn -k uvicorn.workers.UvicornWorker --workers 1 --bind 127.0.0.1:8000 -m 007 app:app
ExecReload=/bin/kill -s HUP \$MAINPID
Restart=on-failure
KillMode=mixed
PrivateTmp=true

[Install]
WantedBy=multi-user.target

EOF
	systemctl daemon-reload
	systemctl start open-attribution-api.service
}

# Assemble python superset frontend systemd service file and starts it
#Environment=${PYTHON_ENV_DIR}/bin
function start-superset {
	echo "Start python superset service"
	cat <<EOF >/etc/systemd/system/open-attribution-superset.service
[Unit]
Description=Open Attribution Superset Analytics Dash for embedding
After=network.target

[Service]
RuntimeDirectory=gunicorn-superset
Environment="SUPERSET_CONFIG_PATH=/home/james/open-attribution/apps/superset/superset_config.py"
WorkingDirectory=${app_dir}/apps/superset
Environment="SUPERSET_CONFIG_PATH=/home/james/open-attribution/apps/superset/superset_config.py"
ExecStart=${PYTHON_ENV_DIR}/bin/gunicorn -w 10 \
                                       -k gevent \
                                       --timeout 120 \
                                       --bind localhost:8088 \
                                       --limit-request-line 0 \
                                       --limit-request-field_size 0 \
                                       "superset.app:create_app()"
ExecReload=/bin/kill -s HUP \$MAINPID
Restart=on-failure
KillMode=mixed
PrivateTmp=true

[Install]
WantedBy=multi-user.target

EOF
	systemctl daemon-reload
	systemctl start open-attribution-superset.service
}

function start-service() {
	local my_service=$1
	if [ "$my_service" == "kafka" ]; then
		start-kafka
	elif [ "$my_service" == "clickhouse" ]; then
		start-clickhouse
	elif [ "$my_service" == "superset" ]; then
		start-superset
	elif [ "$my_service" == "api" ]; then
		start-api
	else
		echo "Unknown service: $my_service"
	fi
}

function check-service() {
	local my_service=$1
	my_service_file="/etc/systemd/system/open-attribution-$my_service.service"

	if [ -f "${my_service_file}" ]; then
		echo "${my_service} service already exists ${my_service_file}"
		start-service "$my_service"
	else
		echo "Create service ${my_service_file}"
		start-service "$my_service"
		echo "service added ${my_service_file}"
	fi

	sleep 2

	while true; do
		status=$(systemctl is-active open-attribution-"$my_service".service)

		if [ -z "$status" ]; then
			echo "Error: Unable to retrieve status for open-attribution-${my_service}.service"
			exit 1
		fi

		echo "open-attribution-${my_service} status:${status}"
		if [ "$status" = "activating" ]; then
			echo "open-attribution-${my_service} is activating, sleep 1"
			sleep 1
		elif [ "$status" = "active" ]; then
			dash_address=" "
			if [ "$my_service" = "superset" ]; then
				dash_address="superset: http://localhost:8088"
			fi
			echo "open-attribution-${my_service} is running normally. ${dash_address}"
			break
		elif [ "$status" = "inactive" ]; then
			echo "open-attribution-${my_service}.service is not running (inactive)."
			journalctl -u open-attribution-"${my_service}".service | tail -n 10
			break
		elif [ "$status" = "failed" ]; then
			echo "open-attribution-${my_service} encountered an error (failed)."
			journalctl -u open-attribution-"${my_service}".service | tail -n 10
			break
		else
			echo "Status check ${my_service} returned an unexpected status code: $status"
		fi
	done

}

check-service clickhouse
check-service kafka
check-service api
check-service superset
