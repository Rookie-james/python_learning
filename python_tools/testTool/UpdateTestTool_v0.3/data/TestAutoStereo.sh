#!/bin/sh
#version:v0.0.3

echo "version:v0.0.3"
echo "Test Start!!!"

pkill Daemon
pkill TaskRunner

if [ ! -f "/mnt/adasCriticalData/bak/calibData.yml" ]
then
    echo " Not backup calibData.yml "
else
    mount -o remount,rw /dev/mmcblk0p1 /mnt/adasCriticalData/
    rm /mnt/adasCriticalData/calibData.yml
    rm /mnt/adasCriticalData/depthData.yml
    rm /mnt/adasCriticalData/cameraInfo.json
    
    cp /mnt/adasCriticalData/bak/calibData.yml /mnt/adasCriticalData/
    cp /mnt/adasCriticalData/bak/depthData.yml /mnt/adasCriticalData/
    cp /mnt/adasCriticalData/bak/cameraInfo.json /mnt/adasCriticalData/
fi

if [ ! -f "/mnt/adasUserData/Config/bak/deviceInfo.json" ]
then
    echo " Not backup deviceInfo.json "
else
    rm /mnt/adasUserData/Config/deviceInfo.json
    rm /mnt/adasUserData/Config/cameraInstallParam.yml
    rm /mnt/adasUserData/Config/ldw.yml
    rm /mnt/adasUserData/Config/depthRefine.yml
    rm /mnt/adasUserData/Config/network.conf
    rm /mnt/adasUserData/Config/canProtocol.json
    rm /mnt/adasUserData/Config/autoCalib.yml

    cp /mnt/adasUserData/Config/bak/deviceInfo.json /mnt/adasUserData/Config/
    cp /mnt/adasUserData/Config/bak/cameraInstallParam.yml /mnt/adasUserData/Config/
    cp /mnt/adasUserData/Config/bak/ldw.yml /mnt/adasUserData/Config/
    cp /mnt/adasUserData/Config/bak/depthRefine.yml /mnt/adasUserData/Config/
    cp /mnt/adasUserData/Config/bak/network.conf /mnt/adasUserData/Config/
    cp /mnt/adasUserData/Config/bak/canProtocol.json /mnt/adasUserData/Config/
    cp /mnt/adasUserData/Config/bak/autoCalib.yml /mnt/adasUserData/Config/
fi

stereo="stereo"
echo $stereo

stereoValue="stereoLabel"

cp /mnt/adasUserData/Config/deviceInfo.json /mnt/adasUserData/

sed -i 's/"VideoSource":[^,]*/"VideoSource":"stereoLabel"/' /mnt/adasUserData/deviceInfo.json
sed -e "s@$stereoValue@$stereo@g" -i /mnt/adasUserData/deviceInfo.json

cp /mnt/adasUserData/deviceInfo.json /mnt/adasUserData/Config/
rm /mnt/adasUserData/deviceInfo.json

sync
sleep 1
reboot
echo "Test End!!!"
