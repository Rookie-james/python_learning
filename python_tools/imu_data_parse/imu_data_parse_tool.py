import pandas as pd
import numpy as np
from draw_image_imu import Draw_Image

def read_imu_data(data_path):
    """读取IMU数据，文件格式需要为utf-8编码格式"""
    all_imu_data = pd.read_csv(data_path,sep = '\n')
    print(all_imu_data.head)
    return all_imu_data

def extract_imu_row_counts(imu_data,start_rows,end_rows):
    """提取需要的IMU数据行数"""
    mid_imu_data = imu_data.iloc[start_rows:end_rows,0]
    print(mid_imu_data.head)
    return mid_imu_data

def parse_imu_data(imu_data):
    """从所需数据中提取出真实数据，返回相应的6个列表"""
    accel_x_list = []
    accel_y_list = []
    accel_z_list = []
    gyro_x_list = []
    gyro_y_list = []
    gyro_z_list = []

    for imu_rows in imu_data:
        if imu_rows[:5] == "accel" and imu_rows[6] == "x":
            accel_x = imu_rows.split(' ')[2]
            accel_x_list.append(float(accel_x))
        if imu_rows[:5] == "accel" and imu_rows[6] == "y":
            accel_y = imu_rows.split(' ')[2]
            accel_y_list.append(float(accel_y))
        if imu_rows[:5] == "accel" and imu_rows[6] == "z":
            accel_z = imu_rows.split(' ')[2]
            accel_z_list.append(float(accel_z))
        if imu_rows[:4] == "gyro" and imu_rows[5] == "x":
            gyro_x = imu_rows.split(' ')[2]
            gyro_x_list.append(float(gyro_x))
        if imu_rows[:4] == "gyro" and imu_rows[5] == "y":
            gyro_y = imu_rows.split(' ')[2]
            gyro_y_list.append(float(gyro_y))
        if imu_rows[:4] == "gyro" and imu_rows[5] == "z":
            gyro_z = imu_rows.split(' ')[2]
            gyro_z_list.append(float(gyro_z))
    all_result = [accel_x_list,accel_y_list,accel_z_list,gyro_x_list,gyro_y_list,gyro_z_list]
    return all_result

def print_statistic_result(result_data):
    """将列表数据转为数组，并做统计"""
    for index, result in enumerate(result_data):
        result_array = np.array(result)
        if index == 0:
            params = 'accel_x'
        elif index == 1:
            params = 'accel_y'
        elif index == 2:
            params = 'accel_z'
        elif index == 3:
            params = 'gyro_x'
        elif index == 4:
            params = 'gyro_y'
        elif index == 5:
            params = 'gyro_z'
        print("*"*50)
        print("imu数据{}最大值为：{}".format(params,result_array.max()))
        print("imu数据{}最小值为：{}".format(params,result_array.min()))
        print("imu数据{}平均值为：{}".format(params,result_array.mean()))
        print("imu数据{}方差为：{}".format(params,result_array.var()))
        print("imu数据{}标准差为：{}".format(params,result_array.std()))
        print("imu数据{}中位数为：{}".format(params,np.median(result_array)))
        print("*"*50,'\n')

if __name__ == '__main__':
    imu_data_path = r"E:\imu\t02_tem_imu.txt"
    imu_data = read_imu_data(imu_data_path)    # 读取IMU数据
    start_row = int(input("请输入需要提取数据的起始行数："))
    end_row = int(input("请输入需要提取数据的结束行数："))
    mid_imu_data = extract_imu_row_counts(imu_data,start_row,end_row)    # 提取需要的数据（行数）
    imu_data_result = parse_imu_data(mid_imu_data)    # 从所需数据的解析出所有IMU数据的真实值
    print_statistic_result(imu_data_result)    # 输出IMU数据统计值

    draw_imu_image = Draw_Image()    # 画图
    draw_imu_image.draw_image(imu_data_result)