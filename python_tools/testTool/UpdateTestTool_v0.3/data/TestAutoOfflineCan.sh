#!/bin/sh
#version:v0.0.3

echo "version:v0.0.3"
echo "Test Start!!!"

if [ ! -d "./adas_params" ]
then
    echo "Error : Can not find adas_params. "
elif [ ! -d "./left_images" ]
then
    echo "Error : Can not find left_images. "
elif [ ! -f "./adas_params/calibData.yml" ]
then
    echo "Error : Can not find calibData.yml."
else
    pkill Daemon
    pkill TaskRunner

    mount -o remount,rw /dev/mmcblk0p1 /mnt/adasCriticalData/

    rm /mnt/adasCriticalData/calibData.yml
    rm /mnt/adasCriticalData/depthData.yml
    rm /mnt/adasCriticalData/cameraInfo.json

    cp ./adas_params/calibData.yml /mnt/adasCriticalData/
    cp ./adas_params/depthData.yml /mnt/adasCriticalData/
    cp ./adas_params/cameraInfo.json /mnt/adasCriticalData/

    rm /mnt/adasUserData/Config/deviceInfo.json
    rm /mnt/adasUserData/Config/cameraInstallParam.yml
    rm /mnt/adasUserData/Config/ldw.yml
    rm /mnt/adasUserData/Config/depthRefine.yml
    rm /mnt/adasUserData/Config/network.conf
    rm /mnt/adasUserData/Config/canProtocol.json
    rm /mnt/adasUserData/Config/autoCalib.yml

    cp ./adas_params/deviceInfo.json /mnt/adasUserData/Config/
    cp ./adas_params/cameraInstallParam.yml /mnt/adasUserData/Config/
    cp ./adas_params/ldw.yml /mnt/adasUserData/Config/
    cp ./adas_params/depthRefine.yml /mnt/adasUserData/Config/
    cp ./adas_params/network.conf /mnt/adasUserData/Config/
    cp ./adas_params/canProtocol.json /mnt/adasUserData/Config/
    cp ./adas_params/autoCalib.yml  /mnt/adasUserData/Config/

    offlinePath=`pwd`
    offline="offline"
    zkhyCan="zkhyCanProtocol"
    can="CAN"

    echo $offlinePath
    echo $offline
    echo $zkhyCan
    echo $can

    offlinePathValue="offlinePathLabel"
    offlineValue="offlineLabel"
    offlineZKHYCanValue="zkhyCanProtocolLabel"
    offlineThirdDeviceValue="thirdDeviceLabel"

    sed -i 's/"OfflineImagePath":[^,]*/"OfflineImagePath":"offlinePathLabel"/' /mnt/adasUserData/Config/deviceInfo.json
    sed -e "s@$offlinePathValue@$offlinePath@g" -i /mnt/adasUserData/Config/deviceInfo.json

    sed -i 's/"VideoSource":[^,]*/"VideoSource":"offlineLabel"/' /mnt/adasUserData/Config/deviceInfo.json
    sed -e "s@$offlineValue@$offline@g" -i /mnt/adasUserData/Config/deviceInfo.json

    sed -i 's/"CanProtocol":[^,]*/"CanProtocol":"zkhyCanProtocolLabel"/' /mnt/adasUserData/Config/deviceInfo.json
    sed -e "s@$offlineZKHYCanValue@$zkhyCan@g" -i /mnt/adasUserData/Config/deviceInfo.json

    sed -i 's/"ThirdDeviceInterface":[^,]*/"ThirdDeviceInterface":"thirdDeviceLabel"/' /mnt/adasUserData/Config/deviceInfo.json
    sed -e "s@$offlineThirdDeviceValue@$can@g" -i /mnt/adasUserData/Config/deviceInfo.json

    sync
    sleep 1
    reboot
    echo "Test End!!!"
fi