import autoproxy
import requests
import logging

logging.basicConfig(level=logging.INFO)

proxies = autoproxy.AutoProxy()
proxies.load_proxies()
# proxies.load_proxies_from_file('proxies.json')

# proxies.dump_proxies("proxies.json")

for i in range(min(10, len(proxies.proxies))):
    proxy = proxies.get_proxy()
    print(proxy.to_requests_like())
    try:
        response = requests.get(f"https://httpbin.org/ip", proxies=proxy.to_requests_like(), timeout=10)
        print(response.text)
    except requests.RequestException as e:
        logging.error(f"Proxy {proxy} failed: {e}")