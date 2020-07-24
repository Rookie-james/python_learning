from update_file_by_sftp import get_ssh, get, put, sftp_connect
import os
import shutil
import time

# def device_type():
#
#     ssh = get_ssh("192.168.1.251", 22, "root", "root")
#     stdin, stdout, stderr = ssh.exec_command('cat /etc/hardware_ver')
#     hardware_ver = str(stdout.read(),"utf-8")
#
#     if hardware_ver == '01000000\n' or hardware_ver == '01000001\n':
#         print("S2系列")
#     elif hardware_ver == '01010000\n' or hardware_ver == '01010001\n' :
#         print("infinite2系列")
#     elif hardware_ver == '11111111\n' or hardware_ver == '00000000\n':
#         print("S1系列")

def save_image_exist():

    tool_path = ".\\tools\\"
    ssh = get_ssh("192.168.1.251", 22, "root", "root")
    client, sftp = sftp_connect("root", "root", "192.168.1.251", port=22)

    stdin, stdout, stderr = ssh.exec_command("find /usr/local/bin/save_fpga_data")
    result = str(stdout.read(),'utf-8').split('/')[-1]
    if result == 'save_fpga_data\n':
        pass
    else:
        print("上传抓图工具...")
        ssh.exec_command('mount -o rw,remount /dev/mmcblk0p2 /usr/local/')
        put(sftp,tool_path+"GetImageTool\\save_fpga_data","/usr/local/bin")
        ssh.exec_command('chmod 766 /usr/local/bin/save_fpga_data')


def get_image():

    tool_path = ".\\tools\\"
    ssh = get_ssh("192.168.1.251", 22, "root", "root")
    client, sftp = sftp_connect("root", "root", "192.168.1.251", port=22)

    ssh.exec_command("pkill Daemon")
    ssh.exec_command('pkill ConfigBackuper')
    ssh.exec_command('rm -rf /mnt/adasUserData/snapshot')

    image_num = 10
    while True:
        image_num = int(input("\n请输入抓图数量(10、50、100、300)："))
            # break
        if image_num == 10 or image_num == 50 \
            or image_num == 100 or image_num == 300:
            break
        else:
            print('输入格式不对，请重新输入')
            continue

    chan = ssh.invoke_shell()
    time.sleep(3)

    if image_num == 10:
        print("图像抓取中，请等待...\n")
        chan.send('save_fpga_data -n 10 & \n')
        time.sleep(10)
        # s_output = str(chan.recv(2048000),'utf-8')
        # print(s_output)
    elif image_num == 50:
        print("图像抓取中，请等待...\n")
        chan.send('save_fpga_data -n 50 & \n')
        time.sleep(50)
        # s_output = str(chan.recv(2048000),'utf-8')
        # print(s_output)
    elif image_num == 100:
        print("图像抓取中，请等待...\n")
        chan.send('save_fpga_data -n 100 & \n')
        time.sleep(100)
        # s_output = str(chan.recv(2048000),'utf-8')
        # print(s_output)
    elif image_num == 300:
        print("图像抓取中，请等待...\n")
        chan.send('save_fpga_data -n 300 & \n')
        time.sleep(300)
        # s_output = str(chan.recv(2048000),'utf-8')
        # print(s_output)
    else:
        print("输入有误！")
        pass

    fpgaIsExists = os.path.exists("D:\\fpga_image\\")

    if not fpgaIsExists:
        os.makedirs("D:\\fpga_image\\")
    else:
        snapshotIsExists = os.path.exists("D:\\fpga_image\\snapshot")
        if snapshotIsExists:
            try:
                shutil.rmtree("D:\\fpga_image\\snapshot")
            except Exception as err:
                print(err)
        pass
    print("将图像下载到本地PC端...")
    get(sftp, "/mnt/adasUserData/snapshot", "D:\\fpga_image\\") #将使用FPGA工具抓取的图像下载到PC端

    print("\n将标定数据下载到本地PC端...")
    get(sftp, "/tmp/eepromData/calibData.yml", "D:\\fpga_image\\snapshot")
    get(sftp, "/tmp/eepromData/cameraInfo.json", "D:\\fpga_image\\snapshot")
    get(sftp, "/tmp/eepromData/depthData.yml", "D:\\fpga_image\\snapshot")

    stdin, stdout, stderr = ssh.exec_command('cat /usr/local/etc/adasVersion')
    ver = str(stdout.read(),'utf-8')
    print("adasVersion is: %s" %ver)
    ver_num = int(ver.split(".")[2])
    # print(ver_num)

    if ver_num <= 8:
        shutil.copy(tool_path+'S2\\AlgRemap.dll',"D:\\fpga_image\\snapshot")
        shutil.copy(tool_path+ \
                    'S2\\compareDecodeImage_Ver1.0.0_Time2020.03.26.exe',
                    "D:\\fpga_image\\snapshot")
    elif ver_num > 8:
        shutil.copy(tool_path+'S2\\image_correct.dll',"D:\\fpga_image\\snapshot")
        shutil.copy(tool_path+'S2\\simulate_remap.dll',"D:\\fpga_image\\snapshot")
        shutil.copy(tool_path+ \
                    'S2\\compareDecodeImage_Ver1.1.1_Time2020.05.27.exe',
                    "D:\\fpga_image\\snapshot")


def main():

    print('=========================')
    print('     FPGA编解码测试工具     ')
    print('=========================')
    save_image_exist()
    get_image()
    os.system("pause")

if __name__ == "__main__":
    main()