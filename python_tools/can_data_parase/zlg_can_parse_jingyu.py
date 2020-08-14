#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : WGQ
# @Time    : 2020/8/13 19:57

import os
import pandas as pd

def gci(filepath,path_list):
    #遍历filepath下所有文件，包括子目录
    files = os.listdir(filepath)
    for fi in files:
        fi_d = os.path.join(filepath,fi)
        #isdir和isfile参数必须跟绝对路径
        if os.path.isdir(fi_d):
            gci(fi_d,path_list)
        else:
        # print(os.path.join(filepath,fi_d))
            all_path = os.path.join(filepath,fi_d)
            # print(all_path)
            path_list.append(all_path)
    return path_list

def extract_79f(can_data):
    """参数为DataFrame格式数据，返回结果为帧ID为79f的所有行"""
    try:
        data_79f = can_data.loc[can_data["ID"].isin(['0x0000079f']),:]
        return data_79f
    except Exception as e:
        print(e)
        return False

def extract_7a0(can_data):
    """参数为DataFrame格式数据，返回结果为帧ID为7a0的所有行"""
    try:
        data_7a0 = can_data.loc[can_data["ID"].isin(['0x000007a0']),:]
        return data_7a0
    except Exception as e:
        print(e)
        return False

def err_frame_count(data_frame):
    """
    参数为任意帧ID的DataFrame格式数据
    返回结果为每个帧间隔之间的时间差在100±10ms之外的个数
    """
    pre_time = 0
    index = 0
    data_frame_count = data_frame.shape[0]
    for ind,Time in enumerate(data_frame["时间戳"]):
        # print(ind)
        if ind == 0:    # 处理第一帧时帧间隔过大的情况
            Time_inter = 100
        else:
            current_time = int(Time.split(':')[0])*3600*1000\
                       + int(Time.split(':')[1]) * 60 * 1000\
                       + int(Time.split(':')[-1].split('.')[0]) *1000\
                       + int(Time.split(':')[-1].split('.')[1])
            Time_inter = current_time - pre_time
            if Time_inter < 0:    # 处理时间戳可能为负数的情况
                current_time = (int(Time.split(':')[0])+24)*3600*1000\
                       + int(Time.split(':')[1]) * 60 * 1000\
                       + int(Time.split(':')[-1].split('.')[0]) *1000\
                       + int(Time.split(':')[-1].split('.')[1])
                Time_inter = current_time - pre_time
        pre_time = int(Time.split(':')[0])*3600*1000\
                   + int(Time.split(':')[1]) * 60 * 1000\
                   + int(Time.split(':')[-1].split('.')[0]) *1000\
                   + int(Time.split(':')[-1].split('.')[1])
        if Time_inter > 110 or Time_inter < 90:    # 判断超时的情况
            index+=1
            print("错误帧：{}；时间戳：{}；帧间隔：{}".format(data_frame["ID"].values[0][-3:],Time,Time_inter))
    return index,data_frame_count

def err_and_count_statistic(data_path_list):

    err_79f = 0
    err_7a0 = 0
    count_79f = 0
    count_7a0 = 0
    for can_data_path in data_path_list:

        can_data0 = pd.read_csv(can_data_path,sep='\\t',encoding='GBK',engine='python')
        _79f = extract_79f(can_data0)
        _7a0 = extract_7a0(can_data0)
        print("*"*50)
        err_count_79f = err_frame_count(_79f)
        err_count_7a0 = err_frame_count(_7a0)

        err_79f_index = err_count_79f[0]
        if err_79f_index > 0:
            print("79f超时路径：{}\n79f超时数：{}".format(can_data_path,err_79f_index))
        err_7a0_index = err_count_7a0[0]
        if err_7a0_index > 0:
            print("7a0超时路径：{}\n7a0超时数：{}".format(can_data_path,err_7a0_index))
        err_79f = err_79f + err_79f_index
        err_7a0 = err_7a0 + err_7a0_index
        count_79f = count_79f + err_count_79f[1]
        count_7a0 = count_7a0 + err_count_7a0[1]
    return err_79f,err_7a0,count_79f,count_7a0

if __name__ == '__main__':
    data_path = r"E:\can_data\1"
    err_79f = 0
    err_7a0 = 0
    count_79f = 0
    count_7a0 = 0
    path_list0 = list()
    can_data_path_list = gci(data_path,path_list=path_list0)
    statistic_result = err_and_count_statistic(can_data_path_list)
    print("*"*50)
    print("79f帧间隔不合格的数为：{}".format(statistic_result[0]))
    print("79f帧总帧数为：{}".format(statistic_result[2]))
    print("79f帧合格率为：{}".format(statistic_result[0]/statistic_result[2]))
    print("7a0帧间隔不合格的数为：{}".format(statistic_result[1]))
    print("7a0帧总帧数为：{}".format(statistic_result[3]))
    print("7a0帧合格率为：{}".format(statistic_result[1]/statistic_result[3]))
    print("*"*50)