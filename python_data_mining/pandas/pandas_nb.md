### 1、掌握外部数据的读取

```python
#文本文件的读取
pd.read_csv(filepath_or_buffer, sep=',', header='infer', names=None, usecols=None,skiprows=None, skipfooter=None, converters=None, encoding=None)

# filepath_or_buffer：指定txt文件或csv文件所在的具体路径
# sep：指定原数据集中各字段之间的分隔符，默认为逗号”,”
# header：是否需要将原数据集中的第一行作为表头，默认将第一行用作字段名称 None
# names：如果原数据集中没有字段，可以通过该参数在数据读取时给数据框添加具体的表头
# usecols：指定需要读取原数据集中的哪些变量名
# skiprows：数据读取时，指定需要跳过原数据集开头的行数
# skipfooter：数据读取时，指定需要跳过原数据集末尾的行数
# converters： 用于数据类型的转换（以字典的形式指定）
# encoding：如果文件中含有中文，有时需要指定字符编码
# thousands：千分位分割符，如“，”或者“."

import pandas as pd
path = r"E:\工作学习\pandas_data\data_test01.txt"
result = pd.read_csv(path, sep=',', skiprows=3, skipfooter=4,  encoding='utf-8', converters = {0:str}, engine ='python', thousands = '&')
print(result)

#    id  year  month  day gender occupation  income
# 0  01  1990      3    7      男       销售经理    6000
# 1  02  1989      8   10      女        化妆师    8500
# 2  03  1991     10   10      男       后端开发   13500
# 3  04  1992     10    7      女       前端设计    6500
# 4  05  1985      6   15      男      数据分析师   18000
```



problems：怎么将三列数据整合为“年-月-日”

```python
# 电子表格的读取
pd.read_excel(io, sheetname=0, header=0, skiprows=None, skip_footer=0,
index_col=None, names=None,
na_values=None, thousands=None, convert_float=True)
# io：指定电子表格的具体路径
# sheetname：指定需要读取电子表格中的第几个Sheet，既可以传递整数也可以传递具体的Sheet名称
# header：是否需要将数据集的第一行用作表头，默认为是需要的
# skiprows：读取数据时，指定跳过的开始行数
# skip_footer：读取数据时，指定跳过的末尾行数
# index_col：指定哪些列用作数据框的行索引（标签）
# na_values：指定原始数据中哪些特殊值代表了缺失值
# thousands：指定原始数据集中的千分位符
# convert_float：默认将所有的数值型字段转换为浮点型字段
# converters：通过字典的形式，指定某些列需要转换的形式

io = r"D:\360安全浏览器下载\85248008db516714b1bf03f35db224e6\Python数据分析与挖掘【326758】了解一下数据的基本情况（一）\第9章 pandas模块的介绍\data_test02.xlsx"
result = pd.read_excel(io, sheet_name=0, header=None, converters={0:str})
print(result)

#        0     1   2    3
# 0  00101   儿童裤  黑色  109
# 1  01123  儿童上衣  红色  229
# 2  01010   儿童鞋  蓝色  199
# 3  00100  儿童内衣  灰色  159
```



```python
# 数据库数据的读取
import pd,pymysql
con = pymysql.connect(host=None, user=None, password=‘’, database=None, port=0, charset=‘’)
# host：指定需要访问的MySQL服务器
# user：指定访问MySQL数据库的用户名
# password：指定访问MySQL数据库的密码
# database：指定访问MySQL数据库的具体库名
# port：指定访问MySQL数据库的端口号
# charset：指定读取MySQL数据库的字符集，如果数据库表中含有中文，一般可以尝试将该参数设置为“utf8” 或“gbk”

pd.read_sql(sql,con)
pd.read_sql_table(table_name,con)
# sql：指定SQL查询语句，将根据查询语句的逻辑返回对应的数据框
# con：指定数据库与Python之间的连接器，即通过pymysql.connect函数或pymssql.connect构造的连接器
# table_name：指定数据库中某张表的名称，将根据表名称返回对应的数据框
```



### 2、如何快速地认知数据的概览信息

```python
# 数据量
df.shape
# 变量列表
df.columns
# 变量类型
df.dtypes
# 统计描述
df.describe  
```



### 3、数据子集的筛选与清洗

##### 数据的筛选

```
列的筛选
df.column_name df[‘column_name’]
行的筛选
df.loc[condition,:]
行列的筛选
df.loc[condition,:column_list]
```



##### 数据的清洗

```python
# 数据类型的修改
pd.to_datetime
df.column.astype
# 示例
import pandas as pd

path = r"E:\工作学习\pandas_data\data_test01.txt"
result = pd.read_csv(path, sep=',', skiprows=3, skipfooter=4,  encoding='utf-8', converters = {0:str},engine ='python', thousands = '&')
print(result['year'].dtypes)
# int64
result['year'] = result['year'].astype('int32')
print(result['year'].dtypes)
# int32

# 冗余数据的识别与处理
df.duplicated	# 判断重复数据
df.drop_duplicates	#去除重复项
```



##### 异常值的识别与处理

###### 1、Z得分法

###### 2、分位数法

###### 3、距离法

###### 示例1、https://mp.weixin.qq.com/s/aWTDJtafY9XHZdHdOUaqXw  -K均值聚类异常值识别

###### 示例2：https://mp.weixin.qq.com/s/728HfX6VFi0tN6MBkFrTsA  -KNN识别异常值

##### 缺失值的识别与处理

###### 1、df.isnull		# 判断缺失值，若缺失则返回True

```python
df.isnull().any()		# 返回哪些列包含缺失值
df.isnull().sum()		# 返回各列包含缺失值的总数
```

###### 2、df.fillna		# 缺失值填充

```python
df.fillna(100)		# 常数填充
df.fillna({0:10,1:20,2:30})		# 通过使用字典填充不同列
df.fillna(0,inplace=True)		# 传入inplace=True直接修改原始数据
df2.fillna(method='ffill')		# 用前面的值来填充
df2.fillna(method='bfill',limit=2)		# 显示填充个数
df2.fillna(method="ffill",limit=1,axis=1)	# axis=可以修改填充方向
```



###### 3、df.dropna  

| parameters | 详解                                                         |
| ---------- | ------------------------------------------------------------ |
| axis       | default 0指行,1为列                                          |
| how        | {‘any’, ‘all’}, default ‘any’指带缺失值的所有行;'all’指清除全是缺失值的行 |
| thresh     | int,保留含有int个非空值的行                                  |
| subset     | 对特定的列进行缺失值删除处理                                 |
| inplace    | 这个很常见,True表示就地更改                                  |

### 4、数据的汇总处理







### 5、数据的合并与连接  