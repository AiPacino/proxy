# coding:utf-8
import re

"""这个脚本的作用就是传入网页内容，我们返回一个list，里面有所有的代理ip"""


proxy_pat = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\D+\d{1,5}', re.S)
proxy_address_pat = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', re.S)
proxy_ip_pat = re.compile(r'\d{1,5}', re.M)


def proxyext(content):
    proxylist = []
    for proxy in re.finditer(proxy_pat, content):
        proxy = proxy.group()
        
        proxy_address = re.match(proxy_address_pat, proxy).group()
        proxy_ip =re.match(proxy_ip_pat, proxy[::-1]).group()[::-1]
        proxylist.append(proxy_address+':'+proxy_ip)
    
    return proxylist