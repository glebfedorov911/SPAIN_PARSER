import asyncio
import random
import os
import keyboard

from playwright.async_api import async_playwright


# host = "50.114.181.135"
# port = 63120
# login = "ZcTq1NqyS"
# password = "aaczYwsJU"

host = "p1.mangoproxy.com"
port = 2334
login = "n66063054a6f17c192a006d-zone-custom-region-es"
password = "b151e67bc2b9462683bdab5eb1ff4acc"

async def first_page(page):
    url = "https://sede.administracionespublicas.gob.es/pagina/index/directorio/icpplus"
    await page.goto(url)
    await page.wait_for_selector("#formulario")
    form = await page.query_selector("#formulario")
    action = await form.get_attribute("action")
    await page.goto(action)

async def second_page(page, city):
    await page.wait_for_selector(".sede")
    await asyncio.sleep(random.uniform(3, 5))
    form = await page.query_selector("#form[name=form]")
    options = await page.query_selector_all("option")
    for option in options:
        if await option.inner_text() == city:
            await form.select_option(await option.get_attribute("value"))
            break
    await page.evaluate("envia()")

async def third_page(page, option1, option2):
        await page.wait_for_selector("select")
        await asyncio.sleep(random.uniform(3, 5))
        form = await page.query_selector("#sede[name=sede]")
        options = await page.query_selector_all("optgroup[label='Elegir oficina'] option")
        for option in options:
            if option1 in await option.inner_html():
                await form.select_option(await option.get_attribute("value"))
                break
        
        await page.wait_for_selector("select")
        await asyncio.sleep(random.uniform(3, 5))
        form_tramites = (await page.query_selector(".mf-input__l"))
        options_tramites = (await page.query_selector_all(".mf-input__l option"))
        for option in options_tramites:
            if option2 in await option.inner_html():
                await form_tramites.select_option(await option.get_attribute("value"))
                break

        await page.evaluate("envia()")

async def fourth_page(page):
    await page.wait_for_selector("#btnAccesoClave")
    await asyncio.sleep(random.uniform(3, 5))
    await (await page.query_selector("#btnAccesoClave")).click()

async def fifth_page(page):
    await page.wait_for_selector("body")
    await asyncio.sleep(random.uniform(10, 15))
    await page.evaluate("JAVASCRIPT:selectedIdP('AFIRMA');idpRedirect.submit();")

async def sixth_page(page):
    await asyncio.sleep(10)
    print("сейчас нажму")
    keyboard.press_and_release('enter')
    print("нажал")

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch_persistent_context(
            user_data_dir=r"D:/_.programming/SPAIN_PARSER/data",
            headless=False, 
            proxy={
                "server": f"{host}:{port}",
                "username": login,
                "password": password,
            },
            # args=[
            #     "--ignore-certificate-errors",
            #     "--client-certificate=D:/_.programming/SPAIN_PARSER/combined.pem",
            #     "--allow-insecure-localhost",
            # ]
            args=[
                "--ignore-certificate-errors",
                "--allow-insecure-localhost",
                "--client-certificate=D:/_.programming/SPAIN_PARSER/certY5008755J_DANIL_RUBIN_ciudadano_1647888216976.pem",
                "--client-key=D:/_.programming/SPAIN_PARSER/privY5008755J_DANIL_RUBIN_ciudadano_1647888216976.pem"
            ]
        )
        page = await browser.new_page()
        await page.context.add_cookies([
            {
                'name': 'client-cert',
                'value': 'D:/_.programming/SPAIN_PARSER/combined.pem',
                'url': 'https://sede.administracionespublicas.gob.es'
            }
        ])
        await first_page(page)
        await second_page(page, "Valencia")
        await third_page(page, "CNP COMISARIA PATRAIX EXTRANJERIA, GREMIS, 6, VALENCIA", "POLICIA-TOMA DE HUELLA (EXPEDICIÓN DE TARJETA), RENOVACIÓN DE TARJETA DE LARGA DURACIÓN Y DUPLICADO")
        await fourth_page(page)
        await fifth_page(page)
        await sixth_page(page)

        await asyncio.sleep(5011)
        await browser.close()

asyncio.run(main())