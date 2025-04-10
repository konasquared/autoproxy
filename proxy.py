import requests

class Proxy():
    def __init__(self, protocol, ip, port, is_socks_proxy=False, force_https=False):
        self.force_https = force_https
        self.protocol = protocol
        self.ip = ip
        self.port = port
        self.is_socks_proxy = is_socks_proxy
    
    def to_requests_like(self):
        if self.is_socks_proxy:
            return {
                'http': f"socks5://{self.ip}:{self.port}",
                'https': f"socks5://{self.ip}:{self.port}"
            }
        else:
            obj = {
                self.protocol: f"{self.protocol}://{self.ip}:{self.port}"
            }

            if self.force_https:
                obj['https'] = f"https://{self.ip}:{self.port}"
            
            return obj
    
    def check(self):
        try:
            response = requests.get(f"https://httpbin.org/ip", proxies=self.to_requests_like(), timeout=2)
            if response.status_code == 200:
                return True
        except requests.RequestException as e:
            pass
        return False
    
    def to_json(self):
        return {
            "protocol": self.protocol,
            "ip": self.ip,
            "port": self.port,
            "force_https": self.force_https
        }
    
    def __str__(self):
        return f"{self.protocol}://{self.ip}:{self.port}"
    
    def __repr__(self):
        return f"Proxy({self.protocol}, {self.ip}, {self.port})"