from update_file_by_sftp import get_ssh, get, put, sftp_connect
import os
import shutil
import time
import re

ssh = get_ssh("192.168.1.251", 22, "root", "root")
client, sftp = sftp_connect("root", "root", "192.168.1.251", port=22)

# 抓图数量
i = int(input('请输入抓图数量:'))
# 设置结束条件
p = re.compile(r"fetchFrame task alive...")


chan = ssh.invoke_shell()
time.sleep(3)
chan.send('cd /mnt/adasUserData/ && ./save_fpga_color_ori_remap_dis_disDS_data.elf -n {} & \n'.format(i))
start_time = time.time()
print(start_time)
result_display = ''
chunk = chan.recv(1024)

n = 0
while chunk:
    if time.time() - start_time > n + 3:
        break
    result_display = chunk
    chunk = chan.recv(1024)
    print(str(result_display,'utf-8'))
    if p.search(str(chunk,'utf-8')):
        n += 1
        print('*'*50)
        print("The current images is index:{}".format(n))
        print('*'*50)
        if n == i:
            time.sleep(1)
            break
print('Test end!!!')
chan = ssh.invoke_shell()
chan.send('ls')


