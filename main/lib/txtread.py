# filename: test.py
import os
users = [] # 用来保存从文件中读取的数据
for item in os.listdir('.'): # 遍历指定目录
    if os.path.isfile(item) and item.endswith('.txt'): # 判断是否为.txt文件
        f = open(item) # 打开文件
        for line in f: # 读入文件的每一行
            if line.startswith('用户名'): # 变量初始化
                uid = age = sex = None    
            elif line.startswith("用户id"): # 根据每行开始内容获取数据
                uid = line.split()[1]
            elif line.startswith("年龄"):
                age = line.split()[1]
            elif line.startswith("性别"):
                sex = line.split()[1]
                users.append([uid, age, sex]) # 将所获得的数据以列表的形式追加到数组中
                
        f.close() # 关闭文件
