### 一、数组的构造及其优势

背景：列表只是一种数据的存储容器，它不具有任何计算能力！

```python
# 身高
height = [176,158,163,177,172,169]
# 体重
weight = [82,61,70,69,89,78]

BMI = weight / (height/100)**2

# Traceback (most recent call last):
#  File "C:/Users/zkhy006/PycharmProjects/爬虫/demo/numpy_practice.py", line 6, in <module>
#    BMI = weight / (height/100)**2
# TypeError: unsupported operand type(s) for /: 'list' and 'int'
```

解决方案：

```python
# 解决方案（将两个列表中对应的元素取出来，做数学运算）
BMI = []
for i in range(len(height)):
    BMI.append(weight[i] / (height[i]/100)**2)
print(type(BMI),BMI)

# <class 'list'> [26.47210743801653, 24.435186668803073, 26.346494034400994, 22.024322512687924, 30.08382909680909, 27.309968138370508]
```



#### 1、一维数组

```python
# 将列表转换为数组
Height = np.array(height)
Weight = np.array(weight)

BMI = Weight / (Height/100) ** 2
print(type(BMI),BMI)

# <class 'numpy.ndarray'> [26.47210744 24.43518667 26.34649403 22.02432251 30.0838291  27.30996814]
```

借助于array函数可以将列表或元组转换为数组

##### Tips：数组更快

```python
import numpy as np
import random,time

h = []
w = []
# 生成10000000组身高体重的随机数
for i in range(10000000):
    h.append(random.randint(153,180))
    w.append(random.uniform(51,88))

bmi = []
# 对列表中元素循环遍历做数学运算，并统计耗时
time_now_1 = time.time()
for i in range(10000000):
    bmi.append(w[i]/(h[i]/100)**2)
time_list = time.time() - time_now_1
print("列表循环耗时为：{}".format(time_list))
# 列表循环耗时为：3.895859718322754

H = np.array(h)
W = np.array(w)
# 统计数组方法耗时
time_now_2 = time.time()
BMI = W/(H/100)**2
time_array = time.time() - time_now_2
print("数组方法耗时：{}".format(time_array))
# 数组方法耗时：0.13962841033935547
```



#### 2、二维数组

```python
import numpy as np

# 基于嵌套列表创建二维数组
arr1 = np.array([[1,3,5,7],
                 [2,4,6,8],
                 [11,13,15,17],
                 [12,14,16,18],
                 [100,101,102,103]])

# 基于嵌套元组创建二维数组
arr2 = np.array(((8.5,6,4.1,2,0.7),
                 (1.5,3,5.4,7.3,9),
                 (3.2,3,3.8,3,3),
                 (11.2,13.4,15.6,17.8,19)))

# 二维数组的打印结果
print(arr1,'\n')
# [[  1   3   5   7]
#  [  2   4   6   8]
#  [ 11  13  15  17]
#  [ 12  14  16  18]
#  [100 101 102 103]] 
print(arr2)
# [[ 8.5  6.   4.1  2.   0.7]
#  [ 1.5  3.   5.4  7.3  9. ]
#  [ 3.2  3.   3.8  3.   3. ]
#  [11.2 13.4 15.6 17.8 19. ]]
```



##### 数组元素的返回

1）在一维数组中，列表的所有索引方法都可以使用在数组中，而且还可以使用间断索引
和逻辑索引；
2）在二维数组中，位置索引必须写成[rows,cols]的形式，方括号的前半部分用于锁定二
维数组的行索引，后半部分用于锁定数组的列索引；
3）如果需要获取二维数组的所有行或列元素，那么，对应的行索引或列索引需要用英文
状态的冒号表示；  

```python
import numpy as np 
 
x = np.array([[  0,  1,  2],[  3,  4,  5],[  6,  7,  8],[  9,  10,  11]])  
print ('我们的数组是：')
print (x)
print ('\n')
# 现在我们会打印出大于 5 的元素  
print  ('大于 5 的元素是：')
# 布尔索引（比较运算）
print (x[x >  5])

# 我们的数组是：
# [[ 0  1  2]
#  [ 3  4  5]
#  [ 6  7  8]
#  [ 9 10 11]]

# 大于 5 的元素是：
# [ 6  7  8  9 10 11]
```



```python
import numpy as np 
 
a = np.array([np.nan,  1,2,np.nan,3,4,5])  
# 使用~(取补运算符)来过滤NaN
print (a[~np.isnan(a)])
# [ 1.   2.   3.   4.   5.]
```



##### 数学运算符

| 运算符 | 含义                 | 运算符 | 含义                   |
| :----- | :------------------- | :----- | :--------------------- |
| +      | 数组对应元素的加和   | -      | 数组对应元素的差       |
| *      | 数组对应元素的乘积   | /      | 数组对应元素的商       |
| %      | 数组对应元素商的余数 | //     | 数组对应元素商的整除数 |
| **     | 数组对应元素的幂指数 |        |                        |



##### 比较运算符

| 符号 | 函数                        | 含义                                 |
| ---- | --------------------------- | ------------------------------------ |
| >    | np.greater(arr1,arr2)       | 判断arr1的元素是否大于arr2的元素     |
| >=   | np.greater_equal(arr1,arr2) | 判断arr1的元素是否大于等于arr2的元素 |
| <    | np.less(arr1,arr2)          | 判断arr1的元素是否小于arr2的元素     |
| <=   | np.less_equal(arr1,arr2)    | 判断arr1的元素是否小于等于arr2的元素 |
| ==   | np.equal(arr1,arr2)         | 判断arr1的元素是否等于arr2的元素     |
| !=   | np.not_equal(arr1,arr2)     | 判断arr1的元素是否不等于arr2的元素   |



##### 常用的数学函数

| 函数             | 函数说明                 |
| ---------------- | ------------------------ |
| np.round(arr)    | 对各元素四舍五入         |
| np.sqrt(arr)     | 计算各元素的算术平方根   |
| np.square(arr)   | 计算各元素的平方值       |
| np.exp(arr)      | 计算以e为底的指数        |
| np.power(arr, α) | 计算各元素的指数         |
| np.log2(arr)     | 计算以2为底各元素的对数  |
| np.log10(arr)    | 计算以10为底各元素的对数 |
| np.log(arr)      | 计算以e为底各元素的对数  |



##### 常用的统计函数

| 函数                 | 函数说明               |
| -------------------- | ---------------------- |
| np.min(arr,axis)     | 按照轴的方向计算最小值 |
| np.max(arr,axis)     | 按照轴的方向计算最大值 |
| np.mean(arr,axis)    | 按照轴的方向计算平均值 |
| np.median(arr,axis ) | 按照轴的方向计算中位数 |
| np.sum(arr,axis)     | 按照轴的方向计算和     |
| np.std(arr,axis)     | 按照轴的方向计算标准差 |
| np.var(arr,axis)     | 按照轴的方向计算方差   |

###### 注意： axis=0时， 计算数组各列的统计值；axis=1时， 计算数组各行的统计值  

```python
# 构造3×3的二维矩阵
arr4 = np.array([[1,1000,3000],[2,20,200],[3,30,300]])
print(arr4)
print('垂直方向计算数组的和： \n',np.sum(arr4,axis = 0))
print('水平方向计算数组的和： \n',np.sum(arr4, axis = 1))

# [[ 1 1000 3000]
# [ 2 20 200]
# [ 3 30 300]]
# 垂直方向（列）计算数组的和：
# [6 1050 3500]
# 水平方向（行）计算数组的和：
# [4001 222 333]
```



##### 几个典型的随机数生成函数

```python
import numpy as np
# 随机整数
np.random.randint()
# 随机均匀分布
np.random.randuniform()
# 随机正态分布
np.random.normal()
```



### 二、常用的数学函数与统计函数

