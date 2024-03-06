#!/bin/bash

# This script is used when deploying the commercial site found at openattribution.dev
# Run starts from .github/workflows/actions-deploy-www.yml

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
SupplementaryGroups=nginx
Environment=NODE_ENV=production PORT=4000
ExecStart=/usr/bin/node /home/openattribution/open-attribution/apps/www/build
Restart=on-failure
KillMode=mixed

[Install]
WantedBy=multi-user.target

EOF
	systemctl daemon-reload
	systemctl restart open-attribution-www.service
	systemctl enable /etc/systemd/system/open-attribution-www.service
}

# Start systemd service
start-service-www

echo "open-attribution-www.service set up finished"
