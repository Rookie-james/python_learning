#!/bin/sh
#version:v0.0.3

echo "version:v0.0.3"
echo "Test Start!!!"

#pkill Daemon
#pkill TaskRunner

mount -o remount,rw /dev/mmcblk0p1 /mnt/adasCriticalData/

rm -r /mnt/adasCriticalData/bak
mkdir /mnt/adasCriticalData/bak
cp /mnt/adasCriticalData/calibData.yml /mnt/adasCriticalData/bak
cp /mnt/adasCriticalData/depthData.yml /mnt/adasCriticalData/bak
cp /mnt/adasCriticalData/cameraInfo.json /mnt/adasCriticalData/bak

rm -r /mnt/adasUserData/Config/bak
mkdir /mnt/adasUserData/Config/bak
cp /mnt/adasUserData/Config/deviceInfo.json /mnt/adasUserData/Config/bak/
cp /mnt/adasUserData/Config/cameraInstallParam.yml /mnt/adasUserData/Config/bak/
cp /mnt/adasUserData/Config/ldw.yml /mnt/adasUserData/Config/bak/
cp /mnt/adasUserData/Config/depthRefine.yml /mnt/adasUserData/Config/bak/
cp /mnt/adasUserData/Config/network.conf /mnt/adasUserData/Config/bak/
cp /mnt/adasUserData/Config/canProtocol.json /mnt/adasUserData/Config/bak/
cp /mnt/adasUserData/Config/autoCalib.yml /mnt/adasUserData/Config/bak/

sync
sleep 1
echo "Test End!!!"