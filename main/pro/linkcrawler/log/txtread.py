# coding:utf-8
# filename: test.py
import os
import re

proxy = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\D+\d{1,5}', re.S)

users = [] # 用来保存从文件中读取的数据
for item in os.listdir('./proxy/'): # 遍历指定目录
    if not os.path.isfile(item) and item.endswith('.txt'): # 判断是否为.txt文件
        f = open('./proxy/'+ item) # 打开文件
        for line in f: # 读入文件的每一行
            print(line)
            _proxy = re.match(proxy,line).group()
            print(_proxy)
            break

        f.close() # 关闭文件
