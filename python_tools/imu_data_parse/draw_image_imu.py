import matplotlib.pyplot as plt
import numpy as np

class Draw_Image():

    def __init__(self):
        plt.figure(figsize=(12,6))
        plt.rcParams['font.sans-serif']=['SimHei']  # 显示中文
        plt.rcParams['axes.unicode_minus']=False  # 显示负号
        pass

    def draw_image(self,imu_result_data):
        """画图，画出每个IMU数据的散点图和线性拟合线"""
        for index,result in enumerate(imu_result_data):
            result_array = np.array(result)
            if index == 0:
                params1 = 'accel_x'
                params2 = '加速度'
                ax = plt.subplot2grid(shape=(2,3),loc=(0,index))
            elif index == 1:
                params1 = 'accel_y'
                params2 = '加速度'
                ax = plt.subplot2grid(shape=(2,3),loc=(0,index))
            elif index == 2:
                params1 = 'accel_z'
                params2 = '加速度'
                ax = plt.subplot2grid(shape=(2,3),loc=(0,index))
            elif index == 3:
                params1 = 'gyro_x'
                params2 = '角速度'
                ax = plt.subplot2grid(shape=(2,3),loc=(1,index-3))
            elif index == 4:
                params1 = 'gyro_y'
                params2 = '角速度'
                ax = plt.subplot2grid(shape=(2,3),loc=(1,index-3))
            elif index == 5:
                params1 = 'gyro_z'
                params2 = '角速度'
                ax = plt.subplot2grid(shape=(2,3),loc=(1,index-3))
            ax.scatter(range(1,len(result_array)+1),result_array,5)
            m,b = np.polyfit(range(1,len(result_array)+1),result_array,1)
            ax.plot(range(1,len(result_array+1)),m * range(1,len(result_array+1)) + b,'-',color = 'orangered')
            ax.set_title('{}轴{}'.format(params1.split('_')[-1],params2))
            ax.set_xlabel('imu帧数')
            ax.set_ylabel(params1)
        plt.subplots_adjust(hspace = 0.6, wspace =0.4)
        plt.show()