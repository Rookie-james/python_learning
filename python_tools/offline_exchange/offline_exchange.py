from update_file_by_sftp import get_ssh, get, put, sftp_connect
import os, time, json, subprocess, datetime
# import shutil
# import time
# import json

# def offline_data():
#     image_path = input("请输入图集路径：")
#     ssh = get_ssh("192.168.1.251", 22, "root", "root")
#     stdin, stdout, stderr = ssh.exec_command("cat /etc/hardware_ver/")
#     hardware_ver = str(stdout.read(),"uff-8")
#     if hardware_ver == '01000000\n':
#         config_path =

def offline_path_modify(path1,path2):
    try:
        file_path = path1 + 'deviceInfo.json'
        with open(file_path,'r') as file1:
            file_content = json.loads(file1.read())      #将deviceInfo.json的内容变为字典
            settings_value = file_content['settings']    #拿到键“settings”的值
            settings_value['OfflineImagePath'] = path2  #修改键“OfflineImagePath”（离线图）的路径
            file_content['settings'] = settings_value    #将新的值赋值给键“settings”
            file_content = json.dumps(file_content)      #将字典重新转为str
            # print(file_content)
            file1.close()
            try:
                with open(file_path,'w') as file2:
                    file2.write(file_content)
                    file2.close()
            except Exception as err:
                print(err)
    except Exception as err:
        print(err)
    time.sleep(1)

def offline_exchange():

    data_path = ".\\data\\"
    info_path = ".\\DisplayCompoundFrames-InfoDemo_abort_V1.0"

    # offline_path = input("请输入离线图路径：")
    offline_path = "/mnt/adasUserData/Night_bulecar-VV6/"
    # offline_path = "/mnt/adasUserData/xiaozhangaiwu/"
    client, sftp = sftp_connect("root", "root", "192.168.1.251", port=22)
    get(sftp, '/mnt/adasUserData/Config/deviceInfo.json',data_path)
    # sub_atlas_1 = sftp.listdir("/mnt/adasUserData/xiaozhangaiwu/")

    sub_atlas_1 = sftp.listdir(offline_path)                      #获取一级目录
    print(sub_atlas_1)
    sub_atlas_1.sort(key=lambda x:int(x[0:-1]))                     #对一级目录排序
    # sub_atlas_1.sort(key=lambda x:int(x[1:]))
    print("一级目录包含：%s"%sub_atlas_1)

    time.sleep(1)

    for i in sub_atlas_1:                                          #遍历一级目录

        client, sftp = sftp_connect("root", "root", "192.168.1.251", port=22)
        path_0 = offline_path + i
        print("进入该目录并执行其子图集：%s" %path_0)
        sub_atlas_2 = sftp.listdir(path_0)
        # sub_atlas_2.sort(key=lambda x:int(x[4:]))
        sub_atlas_2.sort(key=lambda x:int(x[0:-1]))                  #对子目录排序
        print("二级目录包含：%s" %sub_atlas_2)

        for j in sub_atlas_2:                                        #遍历二级目录
            print("当前子图集为：%s" %j)

            # while j in sub_atlas_2:                                 #将该子目录的路径拼接到deviceInfo.json
            path_1 = path_0 + '/' +j
            # print("当前运行图集为：%s" %path_1)
            try:
                test_log_path = data_path + "test_log.txt"
                with open(test_log_path, 'a', encoding='UTF-8') as file_log:
                    # time_now = datetime.datetime.now()
                    file_log.write(str(datetime.datetime.now()))
                    file_log.write('\t')
                    file_log.write(path_1)
                    file_log.write('\n')
                    print("当前运行图集为：%s" %path_1)
            except Exception as err:
                print(err)

            offline_path_modify(data_path, path_1)

            while j in sub_atlas_2:                                 #将该子目录的路径拼接到deviceInfo.json
                #将拼接完的目录上传到设备端
                file_path = data_path + 'deviceInfo.json'
                try:
                    ssh = get_ssh("192.168.1.251", 22, "root", "root")
                    client, sftp = sftp_connect("root", "root", "192.168.1.251", port=22)
                    ssh.exec_command('pkill Daemon')
                    chan = ssh.invoke_shell()
                    time.sleep(3)
                    chan.send('rm -rf /mnt/adasUserData/Config/deviceInfo.json & \n')
                    time.sleep(1)
                    put(sftp, file_path, "/mnt/adasUserData/Config")
                    print('\n')
                    ssh.exec_command('sync')
                    time.sleep(1)
                    ssh.exec_command("reboot")
                    break                                                 #运行正常则跳出while，进入sleep()
                except Exception as err:
                    print(err)
                    continue                                              #若设备断开连接错误则重新连接
            # subprocess.call("E:\workspace\SDK\\v0.2.26\Sdk-Release_msvc2017_64_v0.2.26\\" +
            #                 "Sdk-Release_msvc2017_64_v0.2.26\Runtime\Bin\ObstacleInfoDemo.exe")
            subprocess.call(info_path + "\\Runtime\\Bin\\DisplayCompoundFrames-InfoDemo.exe")
            # time.sleep(80)
    os.system("pause")


if __name__ == "__main__":
    offline_exchange()