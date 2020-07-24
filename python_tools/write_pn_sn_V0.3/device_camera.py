from update_file_by_sftp import get_ssh, put, sftp_connect, disconnect
import time

def splice_field(pn, sn, file_path, device_or_camera):

    """将输入的PN、SN字段拼接到相应文件内"""

    try:
        with open(file_path, 'w') as file:

            if device_or_camera == 'device':
                a = '11P' + sn + '+' + '18P' + pn + '+' + \
                    '16D20200422+01H001.000.001+02Sa2.12.4.0' + '\n'
                file.write(a)
                print('"device_num.txt"中的信息为: %s'%a)

            elif device_or_camera == 'camera':
                a = '11P' + sn + '+' + '18P' + pn+ '\n'
                file.write(a)
                print('"cameraID.txt"中信息为: %s'%a)

    except Exception as error:
        print(error)

def device_camera_num():

    """分体相机，修改设备端、相机端PN/SN号"""

    device_pn = input('请输入设备PN号：')
    device_sn = input('请输入设备SN号：')
    camera_pn = input('请输入相机PN号：')
    camera_sn = input('请输入相机SN号：')

    data_path = ".\\data\\"
    device_info_path = data_path + "device_num" + ".txt"
    camera_info_path = data_path + "cameraID" + ".txt"


    # 输入为空时，默认复用上次输入内容
    if len(device_pn) == 0:

        try:
            with open(device_info_path,'r') as file:
                a = file.read()
                device_pn = a.split('+')[1][3:]
        except Exception as error:
            print(error)

    if len(device_sn) == 0:
        try:
            with open(device_info_path,'r') as file:
                a = file.read()
                device_sn = a.split('+')[0][3:]
        except Exception as error:
            print(error)

    if len(camera_pn) == 0:
        try:
            with open(camera_info_path,'r') as file:
                a = file.read()
                camera_pn = a.split('+')[1][3:]
        except Exception as error:
            print(error)

    if len(camera_sn) == 0:
        try:
            with open(camera_info_path,'r') as file:
                a = file.read()
                camera_sn = a.split('+')[0][3:]
        except Exception as error:
            print(error)

    splice_field(device_pn, device_sn, device_info_path, 'device')
    splice_field(camera_pn, camera_sn, camera_info_path, 'camera')

    ssh = get_ssh("192.168.1.251", 22, "root", "root")
    ssh.exec_command('pkill Daemon')
    ssh.exec_command('pkill ConfigBackuper')

    client, sftp = sftp_connect("root", "root", "192.168.1.251", port=22)
    print("cameraID.txt 文件上传...")
    put(sftp, camera_info_path, "/mnt/adasUserData")
    print("device_num.txt 文件上传...")
    put(sftp, device_info_path, "/mnt/adasUserData")
    print("文件上传完成!")

    chan = ssh.invoke_shell()
    time.sleep(3)
    chan.send('DataAccessor -w /mnt/adasUserData/cameraID.txt & \n')
    time.sleep(1)

    s_output = str(chan.recv(2048),'utf-8')
    print(s_output)
    ssh.exec_command('flashcp /mnt/adasUserData/device_num.txt /dev/mtd6')

    print("PN号、SN号修改完成，设备自动重启！")
    ssh.exec_command('sync')
    ssh.exec_command('rm -rf /mnt/adasUserData/device_num.txt')
    ssh.exec_command('rm -rf /mnt/adasUserData/cameraID.txt')
    ssh.exec_command('reboot')

    ssh.close()

def device_num():

    """一体相机，修改设备端PN/SN号"""

    device_pn = input('请输入设备PN号：')
    device_sn = input('请输入设备SN号：')

    data_path = ".\\data\\"
    device_info_path = data_path + "device_num" + ".txt"

    if len(device_pn) == 0:

        try:
            with open(device_info_path,'r') as file:
                a = file.read()
                device_pn = a.split('+')[1][3:]
        except Exception as error:
            print(error)

    if len(device_sn) == 0:
        try:
            with open(device_info_path,'r') as file:
                a = file.read()
                device_sn = a.split('+')[0][3:]
        except Exception as error:
            print(error)

    splice_field(device_pn, device_sn, device_info_path, 'device')

    ssh = get_ssh("192.168.1.251", 22, "root", "root")

    ssh.exec_command('pkill Daemon')
    ssh.exec_command('pkill ConfigBackuper')

    client, sftp = sftp_connect("root", "root", "192.168.1.251", port=22)

    print("sn.txt 文件上传...")
    put(sftp, device_info_path, "/mnt/adasUserData")
    disconnect(client)
    print("文件上传完成!")

    ssh.exec_command('flashcp /mnt/adasUserData/device_num.txt /dev/mtd6')
    print("PN号、SN号修改完成，设备自动重启！")
    ssh.exec_command('sync')
    ssh.exec_command('rm -rf /mnt/adasUserData/device_num.txt')
    ssh.exec_command('reboot')

    ssh.close()
