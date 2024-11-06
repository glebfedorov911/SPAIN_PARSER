

# for i in range(10):
#     print(i)
#     if i == 7:
#         break
# else:
#     print("всё")


# import requests
# import time

# ip_check_url = "https://httpbin.org/ip"

# proxies = {
#     "http": "http://n66063054a6f17c192a006d-zone-custom-region-es:b151e67bc2b9462683bdab5eb1ff4acc@p1.mangoproxy.com:2334",
#     "https": "http://n66063054a6f17c192a006d-zone-custom-region-es:b151e67bc2b9462683bdab5eb1ff4acc@p1.mangoproxy.com:2334",
# }

# def check_proxy_ip():
#     try:
#         response = requests.get(ip_check_url, proxies=proxies, timeout=10)
#         if response.status_code == 200:
#             return response.json().get("origin")  
#         else:
#             print(f"Ошибка: Код ответа {response.status_code}")
#     except requests.RequestException as e:
#         print(f"Ошибка подключения: {e}")
#     return None

# ip_addresses = set()

# for i in range(5):  
#     ip = check_proxy_ip()
#     if ip:
#         print(f"IP-адрес в запросе {i + 1}: {ip}")
#         ip_addresses.add(ip)
#     time.sleep(5) 

# if len(ip_addresses) > 1:
#     print("Прокси меняет IP-адрес!")
# else:
#     print("IP-адрес остаётся неизменным.")

# import os
# def create_file():
#     path = "hello.txt"
#     if not os.path.exists(path):
#         open(path, 'w')
# create_file()


# from twocaptcha import TwoCaptcha

# solver = TwoCaptcha("1bcccbcfdbbabf371960eec04621f3d4")

# result = solver.normal('image.png')

# print('solved: ' + str(result))


# import pygetwindow as gw
# import time

# windows = gw.getAllWindows()
# windows_enterclick = []

# idx = 0
# for window in windows:
#     if "Загрузки" in window.title:
#         window.activate()
#         time.sleep(2)

import requests
import os
import time
import base64

from bs4 import BeautifulSoup 

from PIL import Image
from io import BytesIO


directory = "captcha"
if not os.path.exists(directory):
    os.mkdir(directory)

url = "https://comforting-nougat-ce99c6.netlify.app/"
html = requests.get(url).text

soup = BeautifulSoup(html, "html.parser")
captcha_url = str(soup.find("img", class_="img-thumbnail").get("src"))
if captcha_url.startswith("data:image"):
    captcha_url = captcha_url.split(",")[1]

image_path = f"{directory}/captcha_{int(time.time())}.png"
captcha_image = base64.b64decode(captcha_url)
image = Image.open(BytesIO(captcha_image))
image.save(image_path, "PNG")

API_KEY = "KEY IN ENV"

from anticaptchaofficial.imagecaptcha import *

solver = imagecaptcha()
solver.set_verbose(1)
solver.set_key(API_KEY)
solver.set_soft_id(0)
solver.set_minLength(5)
solver.set_maxLength(5)

captcha_text = solver.solve_and_return_solution(image_path)
if captcha_text != 0:
    print("captcha text "+captcha_text)
else:
    print("task finished with error "+solver.error_code)