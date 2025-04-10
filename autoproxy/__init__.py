import requests
import json
import random
import logging
import os
import dotenv

from concurrent.futures import ThreadPoolExecutor

dotenv.load_dotenv()

from .proxygenerator import *
from .proxy import Proxy

logger = logging.getLogger(__name__)

def ProxyFromJson(json_obj):
    return Proxy(
        protocol=json_obj['protocol'],
        ip=json_obj['ip'],
        port=json_obj['port'],
        force_https=json_obj.get('force_https', False)
    )

class AutoProxy():
    def __init__(self):
        self.proxies = []
        self.current_idx = 0
        self.proxy_generator = GeonodeSocksProxyGen()

    def get_proxy(self):
        if not self.proxies:
            raise ValueError("No proxies available")
        
        proxy = self.proxies[self.current_idx]
        self.current_idx = (self.current_idx + 1) % len(self.proxies)
        return proxy
    
    def load_proxies(self):
        logger.info("Loading proxies...")
        self.proxy_generator.get_proxies()
        unchecked_proxies = self.proxy_generator.unchecked_proxies

        if not unchecked_proxies:
            raise ValueError("No proxies found")
        
        logger.info(f"Loaded {len(unchecked_proxies)} proxies, starting check...")

        def check_proxy(proxy):
            if proxy.check():
                logger.debug(f"Proxy {proxy.ip}:{proxy.port} is working")
                return proxy
            else:
                logger.debug(f"Proxy {proxy.ip}:{proxy.port} is not working")
                return None

        with ThreadPoolExecutor() as executor:
            results = list(executor.map(check_proxy, unchecked_proxies))
        
        self.proxies = [proxy for proxy in results if proxy is not None]
        logger.info(f"Checked {len(unchecked_proxies)} proxies, found {len(self.proxies)} working proxies")
    
    def get_random_proxy(self):
        if not self.proxies or len(self.proxies) == 0:
            raise ValueError("No proxies available")
        return random.choice(self.proxies)
    
    def dump_proxies(self, filename):
        with open(filename, 'w') as f:
            json.dump([proxy.to_json() for proxy in self.proxies], f)
        
        return random.choice(self.proxies)
    
    def load_proxies_from_file(self, filename):
        with open(filename, 'r') as f:
            data = json.load(f)
        
        self.proxies = [ProxyFromJson(item) for item in data]
        logger.info(f"Loaded {len(self.proxies)} proxies from file")
