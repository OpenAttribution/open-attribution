#!/bin/bash

source ./local.conf

if ! source ./local.conf; then
	echo "Error: Unable to source local.conf. Check you are in open-attribution directory. Copy with: cp example_local.conf local.conf"
	exit 1
fi

# Check if the script is being run as root
if [ "$EUID" -ne 0 ]; then
	echo "Please run as root"
	exit
fi

# This function assembles the kubelet systemd service file and starts it
# using systemctl.
function start-druid {
	echo "Start druid service"
	echo "druid_dir: $DRUID_DIR"
	# Write the systemd service file for kubelet.
	cat <<EOF >/etc/systemd/system/open-attribution-druid.service
[Unit]
Description=Open Attribution Druid service
After=network.target

[Service]
User=james
Group=james
ExecStart=${DRUID_DIR}
ExecReload=/bin/kill -s HUP $MAINPID
Restart=on-failure
KillMode=mixed
PrivateTmp=true

[Install]
WantedBy=multi-user.target

EOF

	systemctl daemon-reload
	systemctl start open-attribution-druid.service

}

app_dir=$(pwd)
echo "setting app_dir to ${app_dir}"
my_link="/etc/systemd/system/open-attribution-druid.service"

if [ -f "${my_link}" ]; then
	echo "Druid service already exists ${my_link}"
	start-druid
else
	echo "Create druid service ${my_link}"
	start-druid
	echo "Druid service added ${my_link}"
fi

systemctl is-active --quiet open-attribution-druid.service >/dev/null 2>&1
status=$?
if [ $status -eq 0 ]; then
	echo "open-attribution-druid is running normally. check http://localhost:8888"
elif [ $status -eq 3 ]; then
	echo "open-attribution-druid.service is not running (inactive)."
	journalctl -u open-attribution-druid.service | tail -n 10
elif [ $status -eq 4 ]; then
	echo "open-attribution-druid encountered an error (failed)."
	journalctl -u open-attribution-druid.service | tail -n 10
else
	echo "Status check returned an unexpected status code: $status"
fi
