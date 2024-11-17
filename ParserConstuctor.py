import asyncio
import random
import keyboard
import aiofiles
import os
import json
import numpy as np
import sounddevice as sd
import time
import base64

from PIL import Image
from io import BytesIO

from pywinauto import Application

from playwright.async_api import async_playwright, TimeoutError

from datetime import datetime

from dotenv import load_dotenv

from anticaptchaofficial.imagecaptcha import *


'''
Инструкция по заполнению JSON:
    Если нужно запустить парсер, то первое поле заполнить - "Запустить парсер"
    Если нужно нажать кнопку, то первое поле заполнить - "Нажать кнопку"
    Если нужно выбрать значение из выпадающего списка, то первое поле заполнить - "Выбрать значение"
    Если нужно воспользоваться альтернативным нажатием на кнопку, то первое поле заполнить - "Альтернативное нажатие"
    Если нужно нажать enter на клавиатуре (при работе с ЭПЦ), то первое поле заполнить - "Нажать enter"
    Если нужно заполнить поле каким-то значением, то первое поле заполнить - "Заполнить поле"
    Если нужно издать звук уведомления - "Прислать уведомление" (вызывать после последней страницы перед бронью) в противном случае прописываем дальнейший функционал
    Если нужно записать дату записи - "Записать дату"
    Если нужно поставить паузу и выполнить действия в ручную - "Поставить задержку"
    Если нужно решить капчу (то есть появится текстовая капча на странице) - "Решить капчу"

Для автоматического выбора номера записи используется id #cita(число) вместо (число) нужно указать время, которое нас устраивает, то есть если там
3 предложенных времени, то нужно указать 1 или 2, или 3.
'''


class ParserConstructor:
    headless = False
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:110.0) Gecko/20100101 Firefox/110.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0",
    ]
    directory = "records"
    filename = f"record.txt"
    path = f"{directory}/{filename}"
    captcha_directory = "captcha"

    def __init__(self, host=None, port=None, login=None, password=None):
        '''Заполнить эти поля, если есть прокси'''
        self.host = host
        self.port = port
        self.login = login
        self.password = password
        self.context = None
        self.browser = None
        self.page = None
        self.playwright = None

        self.create_directories()
        self.create_file()

    def create_directories(self):
        os.makedirs(self.directory, exist_ok=True)
        os.makedirs(self.captcha_directory, exist_ok=True)

    def create_file(self):
        if not os.path.exists(self.path):
            open(self.path, 'w')

    async def button_click(self, selector: str, _id: str = None):
        '''
        selector - селектор html, пример (.uppercase.button_next - клаcc | #btnAceptar - id)
        _id - если у кнопок одинаковые айди/классы, то нужно указать ее номер по счету (НАПРИМЕР КНОПКА ГДЕ ВЫБОР ЭЛЕКТРОННОЙ ПОДПИСИ - ОНА ВТОРАЯ, УКАЗЫВАЕМ 2)
        '''
        try:
            await self.reload_if_reject()
            await self.page.wait_for_selector(selector)
            await asyncio.sleep(random.uniform(1, 2))
            buttons = await self.page.query_selector_all(selector)
            button = buttons[-1] if not _id else buttons[int(_id)-1]
            await self.scroll_to_element(button)
            await button.click()
            print("Все прошло успешно! Нажатие выполнено")
        except TimeoutError as te:
            await self.handle_error("Ошибка! Превышено время ожидания прогрузки страницы!")
        except Exception as e:
            await self.handle_error("Ошибка!", e)

    async def select_option(self, option_value, form_selector, option_selector = None, idx = 1):
        '''
        option_value - значение, которое хотите выбрать в option_selector
        form_selector - селектор html, который указан у тэга <form> или <select>
        option_selector - аналогичен form_selector, исключение если указан optgroup - тогда нужно указывать 
        (У optgroup ОБЯЗАТЕЛЬНО УКАЗАТЬ label (пример, optgroup[label='Elegir oficina']) или что-то подобное/можно попробовать просто optgroup) 
        (оставить пустым, если выбор на странице один)
        '''
        try:
            await self.reload_if_reject()
            await self.page.wait_for_selector(form_selector)
            await asyncio.sleep(random.uniform(1, 2))            
            form = (await self.page.query_selector_all(form_selector))[int(idx)-1]
            await self.scroll_to_element(form)
            await form.click()
            if option_selector:
                options = await self.page.query_selector_all(f"{option_selector} option")
            else:
                options = await self.page.query_selector_all(f"option")

            for option in options:
                if option_value in await option.get_attribute("value") or option_value in await option.inner_text():
                    await asyncio.sleep(random.uniform(.5, 1))
                    await form.select_option(await option.get_attribute("value"))
                    print("Успешно выбрали поле в форме!!")
                    break
            else:
                print("Неверно указан селектор, форма не заполнена")
                raise Exception
        except TimeoutError as te:
            await self.handle_error("Ошибка! Превышено время ожидания прогрузки страницы!")
        except Exception as e:
            await self.handle_error("Ошибка!", e)

    async def alternative_for_next_page(self, _eval):
        '''
        _eval - для примера может быть значение: 
        JAVASCRIPT:selectedIdP('AFIRMA');idpRedirect.submit(); | envia() - Функции onclick() onsubmit() указанные в html тегах
        '''
        try:
            await asyncio.sleep(random.uniform(10, 15))
            await self.page.evaluate(_eval)
            print("Успешно выполнен переход")
        except TimeoutError as te:
            await self.handle_error("Ошибка! Превышено время ожидания прогрузки страницы!")
        except Exception as e:
            await self.handle_error("Ошибка!", e)

    async def click_enter_on_page(self, number):
        '''
        При выборе ЭПЦ необходимо выбрать ее, нужно нажать enter, вызываем эту функцию
        '''
        try:
            await asyncio.sleep(random.uniform(5, 8))

            self.set_front_window()
            await asyncio.sleep(0.5)
            for _ in range(1, int(number)):
                await asyncio.to_thread(keyboard.press_and_release, 'down')
            await asyncio.to_thread(keyboard.press_and_release, 'enter')
            await asyncio.sleep(0.5)

            print("Успешно выполнено нажатие!")
        except TimeoutError as te:
            await self.handle_error("Ошибка! Превышено время ожидания прогрузки страницы!")
        except Exception as e:
            await self.handle_error("Ошибка!", e)

    async def fill_field(self, value_for_fill, selector, idx = None):
        '''
        selector - селектор html, пример (.uppercase.button_next - клаcc | #btnAceptar - id)
        value_for_fill - значение для заполнения поля
        '''
        try:
            await self.reload_if_reject()
            await self.page.wait_for_selector(selector)
            await asyncio.sleep(random.uniform(1, 2))
            field = await self.page.query_selector(selector)
            await self.scroll_to_element(field)
            if isinstance(value_for_fill, list):
                await field.fill(value_for_fill[int(idx)])
            else:
                await field.fill(value_for_fill)
            print("Поле успешно заполенено")
        except TimeoutError as te:
            await self.handle_error("Ошибка! Превышено время ожидания прогрузки страницы!")
        except Exception as e:
            await self.handle_error("Ошибка!", e)

    async def notification(self, time_to_finish = 2):
        '''
        Уведомление
        time_to_finish - Время, после которого парсер продолжит свою работу
        Дефолтное значение = 2 секунда (после звука уведомления)
        '''
        def generate_audio(frequency, duration):
            sample_rate = 44100 
            t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
            audio_data = 0.5 * np.sin(2 * np.pi * frequency * t) 
            return audio_data

        sound_data = generate_audio(frequency=440, duration=1.5)  
        sd.play(sound_data, samplerate=44100)
        await asyncio.sleep(1.5) 
        sd.stop() 
        print(f"До продолжения работы: {int(time_to_finish)} секунд/ы")
        await asyncio.sleep(int(time_to_finish))
        print(f"Время вышло")

    async def save_time_record(self, selector, name):
        '''
        Указать селектор (тот же что в кнопке), чтобы записать дату записи в файл (НО БЕЗ # . ИЛИ ПРОЧЕГО, ПРОСТО ИМЯ)
        name - указать любое значение, которое вам удобно, чтобы ориентироваться в файле
        '''
        await asyncio.sleep(random.uniform(1, 2))
        record_time = await (await self.page.query_selector(f"[for='{selector}']")).inner_text()
        data = {name: record_time.replace("\n", ' ')}
        await self.save_to_file(data)
        print("Данные успешно сохранены в файл")

    async def waiting(self, time):
        '''
        time - время остановки в секундах (ПЕРЕДАВАТЬ В КАВЫЧКАХ!!!)
        '''
        await self.page.wait_for_selector("body")
        print("Ожидание началось", time, "секунд")
        await asyncio.sleep(int(time))
        print("Ожидание кончилось! Продолжаю выполнять действия...")

    async def solve_captchas(self):
        '''
        Указать метод, если на странице ожидается проверка
        '''
        await self.page.wait_for_selector(".img-thumbnail")
        captcha_photo_url = self.convert_bytes_captcha(await (await self.page.query_selector(".img-thumbnail")).get_attribute("src"))
        image_path = self.save_bytes_to_image(captcha_photo_url)
        captcha_text = self.captcha_text(image_path)
        await self.fill_field(captcha_text, "#captcha")
        os.remove(image_path)
        print("Капча разгадана и записана")

    async def start(self, url):
        '''
        Перед написанием всей программы запускаем этот метод, для открытия эмулятора веб версии
        '''
        try:
            self.playwright = await async_playwright().start()
            browser_options = {
                "headless": self.headless,
                "args": [ 
                    "--ignore-certificate-errors",
                    "--allow-insecure-localhost", 
                    r"--client-certificate=D:\_.programming\SPAIN_PARSER\cert\cert.crt",
                    r"--client-key=D:\_.programming\SPAIN_PARSER\cert\private.key",
                    '--disable-blink-features=AutomationControlled', 
                    '--disable-extensions',  
                    '--disable-dev-shm-usage',  
                    '--remote-debugging-port=0',  
                    '--disable-popup-blocking',  
                    '--incognito', 
                    '--disable-web-security',  
                    '--start-maximized',  
                    '--no-sandbox',  
                    '--disable-infobars', 
                ]
            }

            headers = {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "en-US,en;q=0.9",
                "Connection": "keep-alive",
                "Cache-Control": "max-age=0",
            }

            if self.host:
                browser_options["proxy"] = {
                    "server": f"http://{self.host}:{self.port}",
                    "username": self.login,
                    "password": self.password,
                }

            self.browser = await self.playwright.chromium.launch(**browser_options)
            self.context = await self.browser.new_context(
                user_agent=random.choice(self.user_agents), 
                java_script_enabled=True,
                viewport={'width': 1366, 'height': 768}
            )
            self.page = await self.context.new_page()
            self.context.on('route', self.modify_headers)
            await self.context.add_init_script("""
                Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3] });
                Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] });
            """)
            self.page.set_default_timeout(15000)
            await self.page.evaluate("() => { delete navigator.__proto__.webdriver; }")
            await self.page.goto(url)
        except Exception as e:
            await self.handle_error("Ошибка при запуске браузера или переходе на страницу", e)

    async def finish(self):
        '''
        После написания всей программы запускаем этот метод, для закрытия эмулятора веб версии / Вызывается в случае ошибки
        '''
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
        print("Браузер успешно закрыт")

    async def handle_error(self, msg, e=None):
        '''Метод для вызова ошибки и окончания работы парсера'''
        print(f"{msg} | {str(e) if e else ''}")
        await self.finish()
        raise Exception #для перезапуска парсера
    
    async def scroll_to_element(self, element):
        return await self.page.evaluate("""
            (element) => {
                element.scrollIntoView({ behavior: 'smooth', block: 'end' });
            }
        """, element)

    async def save_to_file(self, data):
        async with aiofiles.open(self.path, mode='a', encoding="UTF-8") as f:
            await f.write(str(data) + "\n")

    def save_bytes_to_image(self, url):
        image_path = f"{self.captcha_directory}/captcha_{int(time.time())}.png"
        captcha_image = base64.b64decode(url)
        image = Image.open(BytesIO(captcha_image))
        image.save(image_path, "PNG")
        return image_path

    async def reload_if_reject(self):
        await self.page.wait_for_selector("body")
        body = await self.page.query_selector("body")
        if "The requested URL was rejected. Please consult with your administrador." in await body.inner_text():
            for _ in range(2):
                await self.page.reload()


    @staticmethod
    def captcha_text(path):
        load_dotenv()
        API_KEY = os.getenv("API_KEY")
        LENGTH = 5

        solver = imagecaptcha()
        solver.set_verbose(1)
        solver.set_key(API_KEY)
        solver.set_soft_id(0)
        solver.set_minLength(LENGTH)

        captcha_text = solver.solve_and_return_solution(path)
        return captcha_text

    @staticmethod
    def set_front_window():
        window_title = 'Cl@ve – Chromium'
        app = Application().connect(title_re=window_title)
        windows = app.windows(title_re=window_title)
        windows[0].set_focus()

    @staticmethod
    def convert_bytes_captcha(url):
        if url.startswith("data:image"):
            return url.split(",")[1]

    @staticmethod
    async def modify_headers(route, request):
        headers = request.headers
        headers['sec-fetch-mode'] = 'cors' 
        await route.continue_(headers=headers)