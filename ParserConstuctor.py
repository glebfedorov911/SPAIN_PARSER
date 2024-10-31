import asyncio
import random
import keyboard

from playwright.async_api import async_playwright, TimeoutError


class ParserConstructor:
    def __init__(self, host=None, port=None, login=None, password=None):
        '''Заполнить эти поля, если есть прокси'''
        if host:
            self.browser = await p.chromium.launch_persistent_context(
                headless=False,
                proxy={
                    "server": f"{host}:{port}",
                    "username": login,
                    "password": password,
                },
                args=[
                    "--ignore-certificate-errors",
                    "--allow-insecure-localhost",
                    "--client-certificate=certY5008755J_DANIL_RUBIN_ciudadano_1647888216976.pem",
                    "--client-key=privY5008755J_DANIL_RUBIN_ciudadano_1647888216976.pem"
                ]
            )
        else:
            self.browser = await p.chromium.launch_persistent_context(
                headless=False,
                args=[
                    "--ignore-certificate-errors",
                    "--allow-insecure-localhost",
                    "--client-certificate=certY5008755J_DANIL_RUBIN_ciudadano_1647888216976.pem",
                    "--client-key=privY5008755J_DANIL_RUBIN_ciudadano_1647888216976.pem"
                ]
            )

        self.page = await self.browser.new_page()

    async def button_click(self, selector: str, _id: int = None):
        '''
        selector - селектор html, пример (.uppercase.button_next - клаcc | #btnAceptar - id)
        _id - если у кнопок одинаковые айди/классы, то нужно указать ее номер по счету (НАПРИМЕР КНОПКА ГДЕ ВЫБОР ЭЛЕКТРОННОЙ ПОДПИСИ - ОНА ВТОРАЯ, УКАЗЫВАЕМ 2)
        '''
        try:
            await self.page.wait_for_selector(selector)
            await asyncio.sleep(random.uniform(1, 5))
            buttons = await self.page.query_selector_all(selector)
            button = buttons[-1] if not _id else button[_id-1]
            await button.click()
            print("Все прошло успешно! Переходим на следующую страницу")
            await self.browser.close()
        except TimeoutError as te:
            print("Ошибка! Превышено время ожидания прогрузки страницы!")
            await self.browser.close()
        except Exception as e:
            print("Ошибка!", e)
            await self.browser.close()

    async def select_option(self, option_value, form_selector, option_selector = None):
        '''
        option_value - значение, которое хотите выбрать в option_selector
        form_selector - селектор html, который указан у тэга <form> или <select>
        option_selector - аналогичен form_selector, исключение если указан optgroup - тогда нужно указывать 
        (У optgroup ОБЯЗАТЕЛЬНО УКАЗАТЬ label (пример, optgroup[label='Elegir oficina']) или что-то подобное)
        '''
        try:
            if not option_selector: option_selector = form_selector
            await self.page.wait_for_selector(form_selector)
            await asyncio.sleep(random.uniform(1, 5))
            
            form = await self.page.query_selector(form_selector)
            options = await self.page.query_selector_all(f"{option_selector} option")
            for option in options:
                if option_value in await option.get_attribute("value"):
                    await asyncio.sleep(random.uniform(2, 3))
                    await form.select_option(await option.get_attribute("value"))
                    print("Успешно выбрали поле в форме!!")
                    break
            else:
                print("Неверно указан селектор, форма не заполнена")
                await self.browser.close()
                raise Exception
        except TimeoutError as te:
            print("Ошибка! Превышено время ожидания прогрузки страницы!")
            await self.browser.close()
        except Exception as e:
            print("Ошибка!", e)
            await self.browser.close()

    async def alternative_for_next_page(self, _eval):
        '''
        _eval - для примера может быть значение: 
        JAVASCRIPT:selectedIdP('AFIRMA');idpRedirect.submit(); | envia() - Функции onclink() onsubmit() указанные в html тегах
        '''
        try:
            await self.page.wait_for_selector("body")
            await asyncio.sleep(random.uniform(2, 5))
            await self.page.evaluate(_eval)
            print("Успешно выполнен переход")
        except TimeoutError as te:
            print("Ошибка! Превышено время ожидания прогрузки страницы!")
            await self.browser.close()
        except Exception as e:
            print("Ошибка!", e)
            await self.browser.close()

    async def click_enter_on_page(self):
        '''
        При выборе ЭПЦ необходимо выбрать ее, нужно нажать enter, вызываем эту функцию
        '''
        try:
            await asyncio.sleep(random.uniform(10, 15))
            keyboard.press_and_release('enter')
            print("Успешно выполнено нажатие!")
        except TimeoutError as te:
            print("Ошибка! Превышено время ожидания прогрузки страницы!")
            await self.browser.close()
        except Exception as e:
            print("Ошибка!", e)
            await self.browser.close()

    async def fill_field(self, value_for_fill, selector):
        '''
        selector - селектор html, пример (.uppercase.button_next - клаcc | #btnAceptar - id)
        value_for_fill - значение для заполнения поля
        '''
        try:
            await self.page.wait_for_selector(selector)
            await asyncio.sleep(random.uniform(3, 5))
            field = await page.query_selector(selector)
            await field.fill(value_for_fill)
            print("Поле успешно заполенено")
        except TimeoutError as te:
            print("Ошибка! Превышено время ожидания прогрузки страницы!")
            await self.browser.close()
        except Exception as e:
            print("Ошибка!", e)
            await self.browser.close()
        
    async def finish(self):
        '''
        После написания всей программы запускаем этот метод, для закрытия эмулятора веб версии
        '''
        await self.browser.close()