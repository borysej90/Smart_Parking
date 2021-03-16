#!/bin/bash

# Fetch necessary info 
IP=$(hostname -I | awk '{print $1}')
CURR_FOLDER=$(pwd)
EXEC_FN="${CURR_FOLDER}/rtsp-stream.sh"
SERVICE_FN="/etc/systemd/system/rtsp-stream.service"

# Create service
echo "[Unit]

Description=Auto start RTSP stream

After=multi-user.target

[Service]

Type=simple

ExecStart=$EXEC_FN

User=pi

WorkingDirectory=$CURR_FOLDER

Restart=on-failure

[Install]

WantedBy=multi-user.target
" >> $SERVICE_FN

# Enable service
sudo systemctl enable rtsp-stream.service

# Show RTSP Stream URL
echo "Streamer installed successfully!"
echo "Stream URL: rtsp://${IP}:8554/stream"