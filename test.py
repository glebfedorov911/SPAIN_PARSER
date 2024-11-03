

# for i in range(10):
#     print(i)
#     if i == 7:
#         break
# else:
#     print("всё")


import requests
import time

ip_check_url = "https://httpbin.org/ip"

proxies = {
    "http": "http://n66063054a6f17c192a006d-zone-custom-region-es:b151e67bc2b9462683bdab5eb1ff4acc@p1.mangoproxy.com:2334",
    "https": "http://n66063054a6f17c192a006d-zone-custom-region-es:b151e67bc2b9462683bdab5eb1ff4acc@p1.mangoproxy.com:2334",
}

def check_proxy_ip():
    try:
        response = requests.get(ip_check_url, proxies=proxies, timeout=10)
        if response.status_code == 200:
            return response.json().get("origin")  
        else:
            print(f"Ошибка: Код ответа {response.status_code}")
    except requests.RequestException as e:
        print(f"Ошибка подключения: {e}")
    return None

ip_addresses = set()

for i in range(5):  
    ip = check_proxy_ip()
    if ip:
        print(f"IP-адрес в запросе {i + 1}: {ip}")
        ip_addresses.add(ip)
    time.sleep(5) 

if len(ip_addresses) > 1:
    print("Прокси меняет IP-адрес!")
else:
    print("IP-адрес остаётся неизменным.")