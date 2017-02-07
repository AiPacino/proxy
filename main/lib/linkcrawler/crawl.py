# coding:utf-8

import re
import socket
import Queue
import threading
import sys
import requests
import random
import time

sys.path.append("lib");
from urlfilter import url_is_similar, url_is_repeat, url_contain_custom_focus
socket.setdefaulttimeout(30)
from log import write_log
from source import webcontentext

html = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
gzip = 'gzip, deflate, sdch'
chinese = 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4'
user_agent = ['Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201',
              'Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16',
              'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A',
              'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko',
              'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
              ]

# 已经爬过的链接
crawledurl = []

# 不需要爬的链接
filterurl = ["javascript:void(0);", "#", "javascript:;", "javascript:window.scrollTo(0,0);"]

#爬虫的线程
crawl_queue = Queue.Queue()

# 正则提取href
url_pat = re.compile(r'(?<=href=\").*?(?=\")', re.M)

def get_all_links(page, baseurl, focuskey = ()): 
    """获取整个页面的链接 向队列中加入新url"""

    """"因为这里传入值为page为网页内容，baseurl为页面地址，focuskey为我们要爬取的网站网址"""
    # 从页面中找到所有的url
    for url in re.finditer(url_pat, page):
        print(url)
        url = url.group()

        """如果url在不需要爬取或者已经爬取的网址就跳过"""
        if url in filterurl or url_is_repeat(url):#or url_is_similar(url):
            continue

        """如果是在我们的持续抓取的url中,则我们过来抓取,否则就跳过"""
        if not url_contain_custom_focus(url, focuskey): # 是否含特定域名
            continue
        if url.startswith("http"):
            crawl_queue.put(url)
        else:
            crawl_queue.put(baseurl[:-1]+url)

def random_agent(user_agent):
    """随机选择浏览器user_agent"""
    return random.choice(user_agent)

def check_link(url, focuskey, log, sourcelog):
    """分析链接是否异常 有异常记录到log 没异常获取页面链接"""

    """在已经抓取过的里面添加url"""
    crawledurl.append(url)
    try:
        print(url)
        """发起请求，请求格式为accept为html，可以接受的gzip编码，接受语言为chinese，不要缓存，链接形式是keep-alive，User-Agent是随机的，超时时间为3秒"""
        response = requests.get(url, headers = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*','Accept-Encoding':'identity, deflate, sdch, compress, gzip',
                'Accept-Language':'chinese,en-US,en','Cache-Control':'max-age=0','Connection':'keep-alive',
                'User-Agent':random_agent(user_agent)},timeout = 30)
    except requests.exceptions.ConnectionError:
        write_log(log, 'ConnectionError', url)
    except requests.exceptions.HTTPError:
        write_log(log, 'HTTPError', url)
    except (requests.exceptions.Timeout, socket.timeout):
        write_log(log, "Timeout", url)
    except requests.exceptions.TooManyRedirects:
        write_log(log, 'TooManyRedirects', url)
    except requests.exceptions.InvalidURL:
        write_log(log, 'InvalidURL', url)
    except:
        write_log(log, 'UnknownError', url)
    else:
        """正常响应，获取内容，放入get_all_link(),传入内容为url，可以爬取的名称，抓取的内容"""
        page = response.text
        webcontentext(sourcelog, page, url)
        write_log(log, 'succeed', url)
        get_all_links(page, url, focuskey) # url is base_url

# 定义一个Crawlurl爬取的类
class CrawlUrl(threading.Thread):
    def __init__(self, crawl_queue, focuskey, log, sourcelog):
        # 这里初始化多进程
        threading.Thread.__init__(self)
        self.crawl_queue = crawl_queue
        self.focuskey = focuskey
        self.log = log
        self.sourcelog = sourcelog

    def run(self):
        while True:
            # 首先，我们这里从队列中获取一个url
            url = self.crawl_queue.get()

            # 如果这个url我们还没有验证过
            # 我们就去验证这个网页的各种属性
            if url not in crawledurl:
                check_link(url, self.focuskey, self.log, self.sourcelog)
            self.crawl_queue.task_done()
            ### print "left {}, has {}".format(crawl_queue.qsize(), len(crawledurl))

def main(netloc, focuskey, log, sourcelog):
    for i in range(10):
        crawlthread = CrawlUrl(crawl_queue, focuskey, log, sourcelog)
        
        # 设置此线程是否被主线程守护回收。默认False不回收，需要在 start 方法前调用；
        # 设为True相当于像主线程中注册守护，主线程结束时会将其一并回收
        crawlthread.setDaemon(True)
        crawlthread.start()

        url = netloc
        crawl_queue.put(url)

    crawl_queue.join()

if __name__ == "__main__":
    main(*sys.argv[1:])

