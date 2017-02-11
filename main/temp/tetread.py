# coding:utf-8
# filename: test.py

"""input .txt list proxy output list proxy"""

import os
import re

def reproxylist(path):
    proxy = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\D+\d{1,5}', re.S)

    _proxylist = []

    total = 0 # 用来保存从文件中读取的数据
    for item in os.listdir(path): # 遍历指定目录
        if item.endswith('.txt'): # 判断是否为.txt文件
            f = open(path + item) # 打开文件
            for line in f: # 读入文件的每一行
                _proxy = re.search(proxy,line).group()
                _proxylist.append(_proxy)
            f.close() # 关闭文件

    return _proxylist