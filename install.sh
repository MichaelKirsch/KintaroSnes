#!/bin/bash

function install_script {
    mkdir /opt/kintaro
    cp -i pcb.py /opt/kintaro/pcb.py
    cp -R start /opt/kintaro/start
    cp -i kintarosetup.py /home/pi/kintarosetup.py
    chmod +x /opt/kintaro/pcb.py
    useradd -r -s /bin/false kintaro
    chown -R kintaro:kintaro /opt/kintaro
    cp -i kintaro.service /etc/systemd/system/kintaro.service
    systemctl daemon-reload
    systemctl enable kintaro
    
}

if [[ $EUID -ne 0 ]]; then
  echo "You must be a root user. Try to run the script with sudo" 2>&1
  exit 1
fi
arch=`uname -m`
if [ "$arch" == "armv6l" ] || [ "$arch" == "armv7l" ] 
then
   echo "Raspberry detected"
   install_script
else 
   echo "This script will only run on RaspberryPi"
   exit 1
fi
