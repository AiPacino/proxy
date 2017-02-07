# coding:utf-8

import time
import os
import urlparse
import hashlib
import sys

SIMILAR_SET = set()
REPEAT_SET = set()

def urlformat(url):
    '''
    策略是构建一个三元组
    第一项为url的netloc
    第二项为path中每项的拆分长度
    第三项为query的每个参数名称(参数按照字母顺序排序，避免由于顺序不同而导致的重复问题)
    '''

    # 这里的返回值如果没有子路径，就在url后面添加‘/’
    # example：url = www.baidu.com
    # return url = www.baidu.com/
    if urlparse.urlparse(url)[2] == '':
        url = url+'/'

    #这里我们处理一下我们的url
    #   netloc储存域名
    #   path储存子路径
    #   query储存查询
    url_structure = urlparse.urlparse(url)
    netloc = url_structure[1]
    path = url_structure[2]
    query = url_structure[4]

    temp = (netloc,tuple([len(i) for i in path.split('/')]),tuple(sorted([i.split('=')[0] for i in query.split('&')])))
    # print temp
    return temp


def url_is_similar(url):
    '''
    URL相似性控制

    True url未重复
    False url重复
    '''
    t = urlformat(url)
    if t not in SIMILAR_SET:
        SIMILAR_SET.add(t)
        return False
    return True

def url_is_repeat(url):
    '''
    URL重复控制
    True url未重复
    False url重复
    '''
    if url not in REPEAT_SET:
        REPEAT_SET.add(url)
        return False
    return True

def url_contain_custom_focus(url,focuskey):
    '''
    URL自定义关键字控制  聚焦
    True 符合聚焦策略
    False
    '''
    if len(focuskey) == 0:
        return True
    for i in focuskey:
        if i in url:
            return True
    return False

def netloc_contain_focuskey(url,focuskey):
    if len(focuskey) == 0:
        return True

    url_structure = urlparse.urlparse(url)
    netloc = url_structure[1]

    if focuskey in netloc:
        return True
    return False