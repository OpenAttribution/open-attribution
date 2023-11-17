#!/bin/bash

# Warning: set -e can make debugging tricky
set -e
set -u
set -o pipefail

source ./local.conf

app_dir=$(pwd)
home_dir=$HOME

if ! source ./local.conf; then
	echo "Error: Unable to source local.conf. Check you are in open-attribution directory. Copy with: cp example_local.conf local.conf"
	exit 1
fi

# Check if the script is being run as root
if [ "$EUID" -ne 0 ]; then
	echo "Please run as root"
	exit
fi

# Check & create users: druid, kafka
if ! id "druid" &>/dev/null; then
	sudo useradd -r -s /bin/false druid
	echo "User 'druid' created."
fi

if ! id "kafka" &>/dev/null; then
	sudo useradd -r -s /bin/false kafka
	echo "User 'kafka' created."
fi

# This function assembles the druid systemd service file and starts it
# using systemctl.
function start-druid {
	echo "Start druid service"
	echo "druid_dir: $DRUID_DIR"
	setfacl -R -m u:druid:rwx $DRUID_DIR
	cat <<EOF >/etc/systemd/system/open-attribution-druid.service
[Unit]
Description=Open Attribution Druid service
After=network.target

[Service]
User=druid
Group=druid
ExecStart=${DRUID_DIR}/bin/start-druid
ExecReload=/bin/kill -s HUP \$MAINPID
Restart=on-failure
KillMode=mixed
PrivateTmp=true

[Install]
WantedBy=multi-user.target

EOF

	systemctl daemon-reload
	systemctl start open-attribution-druid.service

}

# This function assembles the kafka systemd service file and starts it
# using systemctl.
function start-kafka {
	echo "Start kafka service"
	echo "kafka_dir: $KAFKA_DIR"
	setfacl -R -m u:druid:rwx $KAFKA_DIR
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

# This function assembles the python litestar api systemd service file and starts it
# using systemctl.
function start-api {
	echo "Start python api service"
	cat <<EOF >/etc/systemd/system/open-attribution-api.service
[Unit]
Description=Gunicorn instance to serve Open Attribution API
After=network.target

[Service]
RuntimeDirectory=gunicorn
WorkingDirectory=${app_dir}
Environment=${home_dir}/venvs/open-attribution-env/bin
ExecStart=${home_dir}/venvs/open-attribution-env/bin/gunicorn -k uvicorn.workers.UvicornWorker --workers 1 --bind 127.0.0.1:8000 -m 007 app:app
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

function start-service() {
	local my_service=$1
	if [ "$my_service" == "kafka" ]; then
		start-kafka
	elif [ "$my_service" == "druid" ]; then
		start-druid
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

	status=$(systemctl is-active open-attribution-"$my_service".service)
	echo "open-attribution-${my_service} status:${status}"
	if [ "$status" = "active" ]; then
		echo "open-attribution-${my_service} is running normally. check http://localhost:8888"
	elif [ "$status" = "inactive" ]; then
		echo "open-attribution-${my_service}.service is not running (inactive)."
		journalctl -u open-attribution-"${my_service}".service | tail -n 10
	elif [ "$status" = "failed" ]; then
		echo "open-attribution-${my_service} encountered an error (failed)."
		journalctl -u open-attribution-"${my_service}".service | tail -n 10
	else
		echo "Status check ${my_service} returned an unexpected status code: $status"
	fi

}

check-service druid
check-service kafka
check-service api
