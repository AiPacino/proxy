# coding:utf-8
import re
from log import write_log
from proxyext import proxyext
"""通过网页内容获取我们需要的值"""
def webcontentext(log, page, url):
    proxylist = proxyext(page)

    if proxylist is None:
        pass
    else:
        for i in proxylist:
            write_log(log, i, url)


