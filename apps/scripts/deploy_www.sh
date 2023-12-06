#!/bin/bash

# This script is used when deploying the commercial site found at openattribution.dev

# Assembles the Kafka systemd service file and starts it
function start-service-www {
	echo "Start open attribution www site service"
	cat <<EOF >/etc/systemd/system/open-attribution-www.service
[Unit]
Description=Using node to serve frontend for Open Attribution Web Site
StartLimitBurst=3
StartLimitIntervalSec=30
After=network.target

[Service]
Type=simple
User=openattribution
Group=openattribution
SupplementaryGroups=www-data
Environment=NODE_ENV=production SOCKET_PATH=/tmp/open-attribution-www.sock
ExecStartPre=/bin/bash -c "sudo rm -f /tmp/open-attribution-www.sock"
ExecStart=/usr/bin/node /home/openattribution/open-attribution/apps/www/build
ExecStartPost=/bin/bash -c "sleep 5 && sudo chown www-data:www-data /tmp/open-attribution-www.sock"
Restart=on-failure
KillMode=mixed

[Install]
WantedBy=multi-user.target

EOF
	systemctl daemon-reload
	systemctl start open-attribution-www.service
	systemctl enable /etc/systemd/system/open-attribution-www.service
}

cd apps || exit
mkdocs build --site-dir www/static/docs
cd www || exit
npm run build

start-service-www
