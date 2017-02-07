# coding:utf-8
import re
import urllib2

url_pat = re.compile(r'(?<=href=\").*?(?=\")', re.M)
proxy_pat = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', re.M)
"""通过网页内容获取我们需要的值"""
def webcontentext(html):
    for url in re.finditer(url_pat, html):
        url = url.group()
        print(url)
    for proxy in re.finditer(proxy_pat, html):
        proxy = proxy.group()
        print(proxy)
    '''    
    doc.text.scan(/\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\D+\d{1,5}/m).each {|item|
        proxyitems[0] = item.match(/\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/).to_s
        proxyitems[1] = item.to_s.reverse.match(/\d{1,5}/m).to_s.reverse
    '''


response = urllib2.urlopen('https://free-proxy-list.net/')
html = response.read()

print(html)
webcontentext(html)
