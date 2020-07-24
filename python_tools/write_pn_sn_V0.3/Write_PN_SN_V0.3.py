"""
    function: this script used to modify Serial Number and Part Number
    auth: wgq
    time: 2020-5-25 20:33:02
    version: v0.0.1
"""
import paramiko
import os
import device_camera
# from device_camera import device_num
# from device_camera import device_camera_num

def main():

    print('=========================')
    print('     PN、SN号修改工具       ')
    print('=========================')

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('192.168.1.251', 22, 'root', 'root')

    stdin, stdout, stderr = ssh.exec_command('cat /etc/hardware_ver')
    hardware_ver = str(stdout.read(),"utf-8")
    print("hardware_ver: %s" %hardware_ver)

    if hardware_ver == '01000000\n' or hardware_ver == '01000001\n' \
            or hardware_ver == '01010000\n' or hardware_ver == '01010001\n' :
        device_camera.device_camera_num()
    else:
        device_camera.device_num()

    os.system("pause")

if __name__ == "__main__":
    main()
