"""
    function: this script used to modify Serial Number and Part Number
    auth: wgq
    time: 2020-5-11 21:00:00
    version: v0.0.1
"""

import time
import os
from update_file_by_sftp import get_ssh

def main():

    ssh = get_ssh("192.168.1.251", 22, "root", "root")

    ssh.exec_command('pkill Daemon')
    ssh.exec_command('fw_setenv active_boot qspiboot ')
    time.sleep(1)
    ssh.exec_command('fw_setenv current_boot qspiboot ')
    time.sleep(1)
    ssh.exec_command('sync')

    print("烧录platform.bin中...")
    ssh.exec_command('flashcp /mnt/adasUserData/platform.bin /dev/mtd8')
    time.sleep(75)
    ssh.exec_command('fw_setenv a_bootable 0')
    time.sleep(1)
    ssh.exec_command('fw_setenv b_bootable 0')
    time.sleep(1)

    ssh.exec_command('sync')
    print("设备重启并进入最小系统！！！")
    ssh.exec_command('reboot')

    ssh.close()
    os.system("pause")
	
if __name__ == "__main__":
    main()
