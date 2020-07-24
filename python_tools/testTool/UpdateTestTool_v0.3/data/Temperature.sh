#!/bin/sh
T=0
while (true)
do
    T=$(awk 'BEGIN{
           C= " '$(cat /sys/bus/iio/devices/iio:device0/in_temp0_raw)' ";
           print int(C*503.975/4096-273.15) }'
       )
    echo "    CPU Temperature =  $T"
	ov491_flashtool -temp
    sleep 1
    clear
done
