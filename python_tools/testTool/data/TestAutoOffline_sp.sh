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
    #mount -o remount,rw /dev/mmcblk0p1 /mnt/adasCriticalData/
    DataAccessor -d calibData.yml
    DataAccessor -d depthData.yml
    #rm /mnt/adasCriticalData/cameraInfo.json

    DataAccessor -w ./adas_params/calibData.yml 
    DataAccessor -w ./adas_params/depthData.yml 
    #DataAccessor -w ./adas_params/cameraInfo.json 

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
	offlineTurnSignalInterfaceValue="TurnSignalLabel"

    sed -i 's/"OfflineImagePath":[^,]*/"OfflineImagePath":"offlinePathLabel"/' ./adas_params/deviceInfo.json
    sed -e "s@$offlinePathValue@$offlinePath@g" -i ./adas_params/deviceInfo.json

    sed -i 's/"VideoSource":[^,]*/"VideoSource":"offlineLabel"/' ./adas_params/deviceInfo.json
    sed -e "s@$offlineValue@$offline@g" -i ./adas_params/deviceInfo.json
	
	sed -i 's/"CanProtocol":[^,]*/"CanProtocol":"zkhyCanProtocolLabel"/' ./adas_params/deviceInfo.json
    sed -e "s@$offlineZKHYCanValue@$zkhyCan@g" -i ./adas_params/deviceInfo.json

    sed -i 's/"ThirdDeviceInterface":[^,]*/"ThirdDeviceInterface":"thirdDeviceLabel"/' ./adas_params/deviceInfo.json
    sed -e "s@$offlineThirdDeviceValue@$can@g" -i ./adas_params/deviceInfo.json

    sed -i 's/"TurnSignalInterface":[^,]*/"TurnSignalInterface":"TurnSignalLabel"/' ./adas_params/deviceInfo.json
    sed -e "s@$offlineTurnSignalInterfaceValue@$can@g" -i ./adas_params/deviceInfo.json
	
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

    sync
    sleep 1
    reboot
    echo "Test End!!!"
 fi