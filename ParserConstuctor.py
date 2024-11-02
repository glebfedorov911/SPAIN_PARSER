import asyncio
import random
import keyboard
import json

from playwright.async_api import async_playwright, TimeoutError

from playsound import playsound


'''
Инструкция по заполнению JSON:
    Если нужно запустить парсер, то первое поле заполнить - "Запустить парсер"
    Если нужно нажать кнопку, то первое поле заполнить - "Нажать кнопку"
    Если нужно выбрать значение из выпадающего списка, то первое поле заполнить - "Выбрать значение"
    Если нужно воспользоваться альтернативным нажатием на кнопку, то первое поле заполнить - "Альтернативное нажатие"
    Если нужно нажать enter на клавиатуре (при работе с ЭПЦ), то первое поле заполнить - "Нажать enter"
    Если нужно заполнить поле каким-то значением, то первое поле заполнить - "Заполнить поле"
    Если нужно издать звук уведомления - "Прислать уведомление" (вызывать после последней страницы перед бронью) в противном случае прописываем дальнейший функционал

Для автоматического выбора номера записи используется id #cita(число) вместо (число) нужно указать время, которое нас устраивает, то есть если там
3 предложенных времени, то нужно указать 1 или 2, или 3.
'''

class ParserConstructor:
    time_to_finish = 7200
    sound_file = "sound/sound.mp3"

    def __init__(self, host=None, port=None, login=None, password=None):
        '''Заполнить эти поля, если есть прокси'''
        self.host = host
        self.port = port
        self.login = login
        self.password = password
        self.browser = None
        self.page = None
        self.playwright = None

    async def button_click(self, selector: str, _id: int = None):
        '''
        selector - селектор html, пример (.uppercase.button_next - клаcc | #btnAceptar - id)
        _id - если у кнопок одинаковые айди/классы, то нужно указать ее номер по счету (НАПРИМЕР КНОПКА ГДЕ ВЫБОР ЭЛЕКТРОННОЙ ПОДПИСИ - ОНА ВТОРАЯ, УКАЗЫВАЕМ 2)
        '''
        try:
            await self.page.wait_for_selector(selector)
            await asyncio.sleep(random.uniform(2, 5))
            buttons = await self.page.query_selector_all(selector)
            button = buttons[-1] if not _id else buttons[_id-1]
            await button.click()
            print("Все прошло успешно! Переходим на следующую страницу")
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
            await asyncio.sleep(random.uniform(2, 5))
            
            form = await self.page.query_selector(form_selector)
            if option_selector:
                options = await self.page.query_selector_all(f"{option_selector} option")
            else:
                options = await self.page.query_selector_all(f"option")

            for option in options:
                if option_value in await option.get_attribute("value") or option_value in await option.inner_text():
                    await asyncio.sleep(random.uniform(2, 3))
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
            await asyncio.sleep(random.uniform(2, 5))
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
            await asyncio.sleep(random.uniform(10, 15))
            keyboard.press_and_release('enter')
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
            await asyncio.sleep(random.uniform(2, 5))
            field = await self.page.query_selector(selector)
            await field.fill(value_for_fill)
            print("Поле успешно заполенено")
        except TimeoutError as te:
            await self.handle_error("Ошибка! Превышено время ожидания прогрузки страницы!")
        except Exception as e:
            await self.handle_error("Ошибка!", e)

    async def notification(self):
        await asyncio.to_thread(playsound, self.sound_file)
        print(f"До закрытия браузера есть: {self.time_to_finish//3600} часа/ов")
        await asyncio.sleep(self.time_to_finish)
        print(f"Время вышло")

    async def start(self, url):
        '''
        Перед написанием всей программы запускаем этот метод, для открытия эмулятора веб версии
        '''
        try:
            self.playwright = await async_playwright().start()
            browser_options = {
                "headless": False,
                "args": [
                    "--ignore-certificate-errors",
                    "--allow-insecure-localhost",
                    "--client-certificate=cert/certY5008755J_DANIL_RUBIN_ciudadano_1647888216976.pem",
                    "--client-key=cert/privY5008755J_DANIL_RUBIN_ciudadano_1647888216976.pem"
                ],
            }

            if self.host:
                browser_options["proxy"] = {
                    "server": f"http://{self.host}:{self.port}",
                    "username": self.login,
                    "password": self.password,
                }

            self.browser = await self.playwright.chromium.launch(**browser_options)
            self.page = await self.browser.new_page()
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

async def parser_worker(queue: asyncio.Queue):
    while True:
        print("Цикл запущен")
        host, port, login, password, worker_data = await queue.get()
        pc = ParserConstructor(host=host, port=port, login=login, password=password)
        time_to_finish = 7200 #секунды

        commands = {
            "Запустить парсер": pc.start,
            "Нажать кнопку": pc.button_click,
            "Выбрать значение": pc.select_option,
            "Альтернативное нажатие": pc.alternative_for_next_page,
            "Нажать enter": pc.click_enter_on_page,
            "Заполнить поле": pc.fill_field,
            "Прислать уведомление": pc.notification,
        }

        try:
            for index_page_data in worker_data:
                data = worker_data[index_page_data]
                args = data[1:]
                if data[0] in commands:
                    await commands[data[0]](*args)
                else:
                    print("Неизвестная команда")
                    break
            await pc.finish()
        except Exception as e:
            print("Ошибка в основном цикле", e if e else '')
            print("Добавляем обратно в очередь")
            await queue.put((host, port, login, password, worker_data))
            await pc.finish()
        finally:
            queue.task_done()

async def main(host, port, login, password, worker_data):
    queue = asyncio.Queue()
    for index_block_parser in worker_data:
        await queue.put((host, port, login, password, worker_data[index_block_parser]))

    workers = [asyncio.create_task(parser_worker(queue=queue)) for _ in range(3)]

    await queue.join()

    for worker in workers:
        worker.cancel()

def read_json(filepath):
    with open(filepath, encoding="utf-8") as file:
        return json.load(file)

if __name__ == "__main__":
    # host = "50.114.181.135"
    # port = 63120
    # login = "ZcTq1NqyS"
    # password = "aaczYwsJU"

    host = "p1.mangoproxy.com"
    port = 2334
    login = "n66063054a6f17c192a006d-zone-custom-region-es"
    password = "b151e67bc2b9462683bdab5eb1ff4acc"

    worker_data = read_json("test.json")
    
    asyncio.run(main(host=host, port=port, login=login, password=password, worker_data=worker_data))