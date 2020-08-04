import pandas as pd

def read_can_log(can_log_path):
    """参数为can数据路径，返回DataFrame结构的数据"""
    try:
        can_data = pd.read_csv(data_path, sep=' ', header = None)
        return can_data
    except Exception as e:
        print(e)
        return False

def extract_79f(can_data):
    """参数为DataFrame格式数据，返回结果为帧ID为79f的所有行"""
    try:
        data_79f = can_data.loc[can_data[7].isin(['ID=0x79f']),:]
        return data_79f
    except Exception as e:
        print(e)
        return False

def extract_7a0(can_data):
    """参数为DataFrame格式数据，返回结果为帧ID为7a0的所有行"""
    try:
        data_7a0 = can_data.loc[can_data[7].isin(['ID=0x7a0']),:]
        return data_7a0
    except Exception as e:
        print(e)
        return False

def extract_7a3(can_data):
    """参数为DataFrame格式数据，返回结果为帧ID为7a3的所有行"""
    try:
        data_7a3 = can_data.loc[can_data[7].isin(['ID=0x7a3']),:]
        return data_7a3
    except Exception as e:
        print(e)
        return False

def time_inter(data_frame):
    """
    参数为任意帧ID的DataFrame格式数据
    返回结果为每个帧间隔之间的时间差在100±10ms之外的个数
    """
    pre_time = 0
    # current_time = 0
    # time_inter = 0
    index = 0
    for time in data_frame[5]:
        current_time = int(time.split(':')[0])
        time_inter = current_time - pre_time
        pre_time = int(time.split(':')[0])
        if time_inter > 110 or time_inter < 90:
            index+=1
    return ("{}帧间隔不合格的数为：{}".format(str(data_frame[7][:1]).split('\n')[0][-3:],index-1))

if __name__ == '__main__':
    data_path = r"D:\ADAS_192.168.1.251_0731_20-49.log"
    data0 = read_can_log(data_path)

    _79f = extract_79f(data0)
    print("79f的数据信息为：{}".format(_79f.info))
    print(time_inter(_79f))
    print("*"*50+'\n')

    _7a0 = extract_7a0(data0)
    print("7a0的数据信息为：{}".format(_7a0.info))
    print(time_inter(_7a0))
    print("*"*50+'\n')

    _7a3 = extract_7a3(data0)
    print("7a3的数据信息为：{}".format(_7a3.info))
    print(time_inter(_7a3))
    print("*"*50+'\n')
