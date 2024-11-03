import asyncio
import random
import os
import keyboard

from playwright.async_api import async_playwright


host = "50.114.181.135"
port = 63120
login = "ZcTq1NqyS"
password = "aaczYwsJU"

# host = "p1.mangoproxy.com"
# port = 2334
# login = "n66063054a6f17c192a006d-zone-custom-region-es"
# password = "b151e67bc2b9462683bdab5eb1ff4acc"

async def first_page(page):
    url = "https://sede.administracionespublicas.gob.es/pagina/index/directorio/icpplus"
    await page.goto(url)
    await page.wait_for_selector("#formulario")
    # form = await page.query_selector("#formulario")
    # action = await form.get_attribute("action")
    # await asyncio.sleep(50000)
    # await page.goto(action)
    await (await page.query_selector(".uppercase.button_next")).click()

async def second_page(page, city):
    await page.wait_for_selector(".sede")
    await asyncio.sleep(random.uniform(3, 5))
    form = await page.query_selector("#form[name=form]")
    options = await page.query_selector_all("option")
    for option in options:
        if await option.inner_text() == city:
            await form.select_option(await option.get_attribute("value"))
            break
    await (await page.query_selector("#btnAceptar")).click() #ДЕЛАТЬ ВЕЗДЕ ТАК!!!!!!

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
    print("сейчас нажму")
    await asyncio.sleep(random.uniform(10, 15))
    keyboard.press_and_release('enter')
    print("нажал")

async def seventh_page(page, code, name, country): 
    await page.wait_for_selector("#txtIdCitado")
    await asyncio.sleep(random.uniform(3, 5))
    nie = await page.query_selector("#txtIdCitado")
    await nie.fill(code)

    nombre = await page.query_selector("#txtDesCitado")
    await asyncio.sleep(random.uniform(3, 5))
    await nombre.fill(name)

    form = await page.query_selector("#txtPaisNac")
    options = await page.query_selector_all("#txtPaisNac option")
    for option in options:
        print(await option.inner_text())
        if country in await option.inner_text():
            await asyncio.sleep(random.uniform(3, 5))
            await form.select_option(await option.get_attribute("value"))
            break
    
    await asyncio.sleep(random.uniform(3, 5))
    await page.evaluate("envia()")

async def eightth_page(page):
    await page.wait_for_selector("#btnEnviar")
    await asyncio.sleep(random.uniform(3, 5))
    await page.click("#btnEnviar")

async def nineth_page(page, phone, email1, email2):
    await page.wait_for_selector(".cajapeque") 
    phone = await page.query_selector(".cajapeque")
    await phone.fill(phone)
    await asyncio.sleep(random.uniform(3, 5))
        
    emailUNO = await page.query_selector("emailUNO")
    await emailUNO.fill(email1)
    await asyncio.sleep(random.uniform(3, 5))

    emailDOS = await page.query_selector("emailDOS")
    await emailDOS.fill(email2)
    await asyncio.sleep(random.uniform(3, 5))

    await page.evaluate("enviar()")

async def tenth_page(page, num): #ВЫБОР ЗАПИСИ!!!!!!!!!
    await page.wait_for_selector("#cita1")
    await asyncio.sleep(random.uniform(5, 8))
    await page.click(f"#cita{num}")
    await asyncio.sleep(random.uniform(5, 8))
    await page.click("#btnSiguiente")
    await asyncio.sleep(random.uniform(5, 8))
    await page.click(".btn.btn-default")

async def eleventh_page(page):
    await page.wait_for_selector("#chkTotal")
    await asyncio.sleep(random.uniform(5, 8))
    await page.click(f"#chkTotal")
    await asyncio.sleep(random.uniform(5, 8))
    await page.click("#enviarCorreo")
    await asyncio.sleep(random.uniform(5, 8))
    await page.evaluate("envia()")

async def twelveth_page(page):
    await page.wait_for_selector("#btnSalir")
    await asyncio.sleep(random.uniform(5, 8))
    await page.click(f"#btnSalir")

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False, 
            proxy={
                "server": f"{host}:{port}",
                "username": login,
                "password": password,
            },
            args=[
                "--ignore-certificate-errors",
                "--allow-insecure-localhost",
                "--client-certificate=D:/_.programming/SPAIN_PARSER/certY5008755J_DANIL_RUBIN_ciudadano_1647888216976.pem",
                "--client-key=D:/_.programming/SPAIN_PARSER/privY5008755J_DANIL_RUBIN_ciudadano_1647888216976.pem"
            ]
        )
        page = await browser.new_page()
        # await page.context.add_cookies([
        #     {
        #         'name': 'client-cert',
        #         'value': 'D:/_.programming/SPAIN_PARSER/combined.pem',
        #         'url': 'https://sede.administracionespublicas.gob.es'
        #     }
        # ])
        await first_page(page)
        await second_page(page, "Valencia")
        await third_page(page, "CNP COMISARIA PATRAIX EXTRANJERIA, GREMIS, 6, VALENCIA", "POLICIA-TOMA DE HUELLA (EXPEDICIÓN DE TARJETA), RENOVACIÓN DE TARJETA DE LARGA DURACIÓN Y DUPLICADO")
        await fourth_page(page)
        await fifth_page(page)
        await sixth_page(page)
        await seventh_page(page, "Y8800766S", "ADA DAS", "ARGELIA")
        await eightth_page(page)
        await nineth_page(page, "612345658", "t2est@gmail.com", "t2est@gmail.com")
        await tenth_page(page, 1)
        await eleventh_page(page)
        await twelveth_page(page)

        await asyncio.sleep(1000)
        await browser.close()

asyncio.run(main())