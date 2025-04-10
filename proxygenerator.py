import requests
import re
import os
import dotenv
from proxy import Proxy


class ProxyGenerator:
    def __init__(self):
        self.unchecked_proxies = []

    def get_proxies(self):
        pass

class GeonodeProxyGen(ProxyGenerator):
    def __init__(self):
        self.unchecked_proxies = []

    def get_proxies(self):
        url = "https://proxylist.geonode.com/api/proxy-list?protocols=https%2Chttp&limit=100&page=1&sort_by=lastChecked&sort_type=desc"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            self.unchecked_proxies = [Proxy(item['protocols'][0], item['ip'], item['port']) for item in data['data']]
        else:
            raise ValueError("Failed to fetch proxies")

class SpysOneHTTPProxyGen(ProxyGenerator):
    def __init__(self):
        self.unchecked_proxies = []

    def get_proxies(self):
        url = "https://spys.me/proxy.txt"

        fetch_number = '2' # 0: 30, 1: 50, 2: 100, 3: 200, 4: 300, 5: 500
        anonymity = '0' # 0: all, 1: anon+elite, 2: non-anon, 3: anon, 4: elite
        ssl = '0' # 0: all, 1: ssl, 2: no-ssl
        port = '0' # 0: all, 1: 3128, 2: 8080, 3: 80
        type = '1' # 0: all, 1: http, 2: socks

        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:136.0) Gecko/20100101 Firefox/136.0'
        }

        response = requests.get(url)

        if response.status_code == 200:
            raw = response.text
        else:
            raise ValueError("Failed to fetch proxies")
        
        lines = raw.split('\n')
        del lines[0:5]
        del lines[-1]
        del lines[-2]

        for line in lines:
            line = line.strip()
            if not line:
                continue
            parts = line.split()

            addr_port = parts[0].split(':')
            addr = addr_port[0]
            port = addr_port[1]

            markers = parts[1].split('-')
            if len(markers) == 3:
                protocol = 'https'
            else:
                protocol = 'http'
            
            if markers[1] == 'N':
                continue # don't want non anon proxies
            
            proxy = Proxy(protocol, addr, port)
            self.unchecked_proxies.append(proxy)
        return self.unchecked_proxies

class SpysOneSocksProxyGen(ProxyGenerator):
    def __init__(self):
        self.unchecked_proxies = []
    
    def get_proxies(self):
        url = "https://spys.me/socks.txt"

        response = requests.get(url)

        if response.status_code == 200:
            raw = response.text
        else:
            raise ValueError("Failed to fetch proxies")
        
        lines = raw.split('\n')
        del lines[0:5]
        del lines[-1]
        del lines[-2]

        for line in lines:
            line = line.strip()
            if not line:
                continue
            parts = line.split()

            addr_port = parts[0].split(':')
            addr = addr_port[0]
            port = addr_port[1]

            markers = parts[1].split('-')
            if len(markers) == 3:
                protocol = 'socks5'
            else:
                protocol = 'socks5'
            
            if markers[1] == 'N':
                #continue # don't want non anon proxies
                pass # ok maybe we do want non anon proxies
            
            proxy = Proxy(protocol, addr, port, is_socks_proxy=True)
            self.unchecked_proxies.append(proxy)
        return self.unchecked_proxies




    
