#!/bin/bash
systemctl stop kintaro
systemctl disable kintaro
systemctl daemon-reload
rm -f /etc/systemd/system/kintaro.service 
rm -Rf /opt/kintaro/
rm -f /home/pi/kintarosetup.py
