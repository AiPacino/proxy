from random import choice

import aiohttp
import asyncio
import async_timeout
import re


SERVER_LIST = ['http://ip.dnsexit.com',
               'http://ifconfig.me/ip',
               'http://ipecho.net/plain',
               'http://checkip.dyndns.org/plain',
               'http://ipogre.com/linux.php',
               'http://whatismyipaddress.com/',
               'http://ip.my-proxy.com/',
               'http://websiteipaddress.com/WhatIsMyIp',
               'http://getmyipaddress.org/',
               'http://www.my-ip-address.net/',
               'http://myexternalip.com/raw',
               'http://www.canyouseeme.org/',
               'http://www.trackip.net/',
               'http://icanhazip.com/',
               'http://www.iplocation.net/',
               'http://www.howtofindmyipaddress.com/',
               'http://www.ipchicken.com/',
               'http://whatsmyip.net/',
               'http://www.ip-adress.com/',
               'http://checkmyip.com/',
               'http://www.tracemyip.org/',
               'http://checkmyip.net/',
               'http://www.lawrencegoetz.com/programs/ipinfo/',
               'http://www.findmyip.co/',
               'http://ip-lookup.net/',
               'http://www.dslreports.com/whois',
               'http://www.mon-ip.com/en/my-ip/',
               'http://www.myip.ru',
               'http://ipgoat.com/',
               'http://www.myipnumber.com/my-ip-address.asp',
               'http://www.whatsmyipaddress.net/',
               'http://formyip.com/',
               'https://check.torproject.org/',
               'http://www.displaymyip.com/',
               'http://www.bobborst.com/tools/whatsmyip/',
               'http://www.geoiptool.com/',
               'https://www.whatsmydns.net/whats-my-ip-address.html',
               'https://www.privateinternetaccess.com/pages/whats-my-ip/',
               'http://checkip.dyndns.com/',
               'http://myexternalip.com/',
               'http://www.ip-adress.eu/',
               'http://www.infosniper.net/',
               'http://wtfismyip.com/',
               'http://ipinfo.io/',
               'http://httpbin.org/ip']


ip_address_matcher = re.compile(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")


async def fetch(session, url):
    with async_timeout.timeout(10):
        async with session.get(url) as response:
            return await response.text()


async def get_external_ip_address(loop):
    async with aiohttp.ClientSession(loop=loop) as session:
        server_address = choice(SERVER_LIST)

        html = await fetch(session, server_address)
        print(html)
        match = ip_address_matcher.search(html)
        if match:
            return match.group()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_external_ip_address(loop))
