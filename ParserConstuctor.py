import asyncio
import random
import keyboard
import aiofiles
import os
import json
import numpy as np
import sounddevice as sd

from fake_useragent import UserAgent

from playwright.async_api import async_playwright, TimeoutError

from datetime import datetime


#ДОБАВИТЬ ЭНДПОИНТПАУЗЫ!!!!!!!!
#СОХРАНЯТЬ ДАТУ ЗАПИСИ
'''
Инструкция по заполнению JSON:
    Если нужно запустить парсер, то первое поле заполнить - "Запустить парсер"
    Если нужно нажать кнопку, то первое поле заполнить - "Нажать кнопку"
    Если нужно выбрать значение из выпадающего списка, то первое поле заполнить - "Выбрать значение"
    Если нужно воспользоваться альтернативным нажатием на кнопку, то первое поле заполнить - "Альтернативное нажатие"
    Если нужно нажать enter на клавиатуре (при работе с ЭПЦ), то первое поле заполнить - "Нажать enter"
    Если нужно заполнить поле каким-то значением, то первое поле заполнить - "Заполнить поле"
    Если нужно издать звук уведомления - "Прислать уведомление" (вызывать после последней страницы перед бронью) в противном случае прописываем дальнейший функционал
    Если хотите записать дату записи - "Записать дату"
    Если хотите поставить паузу и выполнить действия в ручную - "Поставить задержку"

Для автоматического выбора номера записи используется id #cita(число) вместо (число) нужно указать время, которое нас устраивает, то есть если там
3 предложенных времени, то нужно указать 1 или 2, или 3.
'''

class ParserConstructor:
    time_to_finish = 7200
    headless = False
    ua = UserAgent()
    directory = "records"
    filename = f"record.txt"
    path = f"{directory}/{filename}"

    def __init__(self, host=None, port=None, login=None, password=None, client_cerf=None, client_key=None):
        '''Заполнить эти поля, если есть прокси'''
        self.host = host
        self.port = port
        self.login = login
        self.password = password
        self.client_cerf = client_cerf
        self.client_key = client_key
        self.context = None
        self.browser = None
        self.page = None
        self.playwright = None

        self.create_directory()
        self.create_file()

    def create_directory(self):
        os.makedirs(self.directory, exist_ok=True)

    def create_file(self):
        if not os.path.exists(self.path):
            open(self.path, 'w')

    async def button_click(self, selector: str, _id: int = None):
        '''
        selector - селектор html, пример (.uppercase.button_next - клаcc | #btnAceptar - id)
        _id - если у кнопок одинаковые айди/классы, то нужно указать ее номер по счету (НАПРИМЕР КНОПКА ГДЕ ВЫБОР ЭЛЕКТРОННОЙ ПОДПИСИ - ОНА ВТОРАЯ, УКАЗЫВАЕМ 2)
        '''
        try:
            await self.page.wait_for_selector(selector)
            await asyncio.sleep(random.uniform(1, 3))
            buttons = await self.page.query_selector_all(selector)
            button = buttons[-1] if not _id else buttons[_id-1]
            await button.click()
            print("Все прошло успешно! Нажатие выполнено")
        except TimeoutError as te:
            await self.handle_error("Ошибка! Превышено время ожидания прогрузки страницы!")
        except Exception as e:
            await self.handle_error("Ошибка!", e)

    async def select_option(self, option_value, form_selector, option_selector = None):
        '''
        option_value - значение, которое хотите выбрать в option_selector
        form_selector - селектор html, который указан у тэга <form> или <select>
        option_selector - аналогичен form_selector, исключение если указан optgroup - тогда нужно указывать 
        (У optgroup ОБЯЗАТЕЛЬНО УКАЗАТЬ label (пример, optgroup[label='Elegir oficina']) или что-то подобное/можно попробовать просто optgroup) 
        (оставить пустым, если выбор на странице один)
        '''
        try:
            await self.page.wait_for_selector(form_selector)
            await asyncio.sleep(random.uniform(1, 3))
            
            form = await self.page.query_selector(form_selector)
            if option_selector:
                options = await self.page.query_selector_all(f"{option_selector} option")
            else:
                options = await self.page.query_selector_all(f"option")

            for option in options:
                if option_value in await option.get_attribute("value") or option_value in await option.inner_text():
                    await asyncio.sleep(random.uniform(1, 2))
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
            await self.page.wait_for_selector("body")
            await asyncio.sleep(random.uniform(1, 3))
            await self.page.evaluate(_eval)
            print("Успешно выполнен переход")
        except TimeoutError as te:
            await self.handle_error("Ошибка! Превышено время ожидания прогрузки страницы!")
        except Exception as e:
            await self.handle_error("Ошибка!", e)

    async def click_enter_on_page(self):
        '''
        При выборе ЭПЦ необходимо выбрать ее, нужно нажать enter, вызываем эту функцию
        '''
        try:
            await asyncio.sleep(random.uniform(8, 10))
            await asyncio.to_thread(keyboard.press_and_release, 'enter')
            print("Успешно выполнено нажатие!")
        except TimeoutError as te:
            await self.handle_error("Ошибка! Превышено время ожидания прогрузки страницы!")
        except Exception as e:
            await self.handle_error("Ошибка!", e)

    async def fill_field(self, value_for_fill, selector):
        '''
        selector - селектор html, пример (.uppercase.button_next - клаcc | #btnAceptar - id)
        value_for_fill - значение для заполнения поля
        '''
        try:
            await self.page.wait_for_selector(selector)
            await asyncio.sleep(random.uniform(1, 3))
            field = await self.page.query_selector(selector)
            await field.fill(value_for_fill)
            print("Поле успешно заполенено")
        except TimeoutError as te:
            await self.handle_error("Ошибка! Превышено время ожидания прогрузки страницы!")
        except Exception as e:
            await self.handle_error("Ошибка!", e)

    async def notification(self):
        '''
        Уведомление
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
        print(f"До закрытия браузера есть: {self.time_to_finish // 3600} часа/ов")
        await asyncio.sleep(self.time_to_finish)
        print(f"Время вышло")

    async def save_time_record(self, selector, name):
        '''
        Указать селектор (тот же что в кнопке), чтобы записать дату записи в файл (НО БЕЗ # . ИЛИ ПРОЧЕГО, ПРОСТО ИМЯ)
        name - указать любое значение, которое вам удобно, чтобы ориентироваться в файле
        '''
        await asyncio.sleep(random.uniform(1, 3))
        record_time = await (await self.page.query_selector(f"[for='{selector}']")).inner_text()
        data = {name: record_time.replace("\n", ' ')}
        await self.save_to_file(data)
        print("Данные успешно сохранены в файл")

    async def waiting(self, time):
        '''
        time - время остановки в секундах (ПЕРЕДАВАТЬ В КАВЫЧКАХ!!!)
        '''
        await asyncio.sleep(int(time))
        print("Ожидание кончилось! Продолжаю выполнять действия...")

    async def start(self, url):
        '''
        Перед написанием всей программы запускаем этот метод, для открытия эмулятора веб версии
        '''
        try:
            self.playwright = await async_playwright().start()
            browser_options = {
                "headless": self.headless,
            }

            if self.client_cerf and self.client_key:
                browser_options["args"] = [
                    "--ignore-certificate-errors",
                    "--allow-insecure-localhost", 
                    f"--client-certificate=cert/{self.client_cerf}", 
                    f"--client-key=cert/{self.client_key}"
                ],

            if self.host:
                browser_options["proxy"] = {
                    "server": f"http://{self.host}:{self.port}",
                    "username": self.login,
                    "password": self.password,
                }

            self.browser = await self.playwright.chromium.launch(**browser_options)
            self.context = await self.browser.new_context(user_agent=self.ua.random)
            self.page = await self.context.new_page()
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
    
    async def save_to_file(self, data):
        async with aiofiles.open(self.path, mode='a', encoding="UTF-8") as f:
            await f.write(str(data) + "\n")