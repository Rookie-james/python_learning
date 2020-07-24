"""
    function: this script used to modify Serial Number and Part Number
    auth: wgq
    time: 2020-4-22 17:33:02
    version: v0.0.1
"""
from update_file_by_sftp import put, sftp_connect, disconnect
import os
import paramiko


def get_ssh(host, port, user_name, passwd):
    """
        function: this interface used to login server by user name and passwd
    """
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, port, user_name, passwd)

    return ssh


def main():

    PN = input('请输入设备PN号：')
    SN = input('请输入设备SN号：')

    data_path = ".\\data\\"
    SN_path = data_path + "sn" + ".txt"

    if len(PN) == 0:
        try:
            with open(SN_path,'r') as file:
                a = file.read()
                PN = a.split('+')[1][3:]
        except Exception as error:
            print(error)
        finally:
            file.close()


    if len(SN) == 0:
        try:
            with open(SN_path,'r') as file:
                a = file.read()
                SN = a.split('+')[0][3:]
        except Exception as error:
            print(error)
        finally:
            file.close()

    try:
        with open(SN_path,'w') as file:

            # if len(SN) == 0:
            #     a =
            a = '11P' + SN + '+' + '18P' + PN + '+' + '16D20200422+01H001.000.001+02Sa2.12.4.0' + '\n'
            # a = '11P' + SN + '+' + '18P' + PN + '\n'
            file.write(a)
            print('"sn.txt"中信息为: %s'%a)

    except Exception as error:
        print(error)

    finally:
        file.close()

    ssh = get_ssh("192.168.1.251", 22, "root", "root")

    ssh.exec_command('pkill Daemon')
    ssh.exec_command('pkill ConfigBackuper')

    client, sftp = sftp_connect("root", "root", "192.168.1.251", port=22)

    print("sn.txt 文件上传...")
    put(sftp, SN_path, "/mnt/adasUserData")
    disconnect(client)
    print("文件上传完成!")

    ssh.exec_command('flashcp /mnt/adasUserData/sn.txt /dev/mtd6')
    print("PN号、SN号修改完成，设备自动重启！")
    ssh.exec_command('sync')
    ssh.exec_command('reboot')

    ssh.close()

    os.system("pause")

if __name__ == "__main__":
    main()
