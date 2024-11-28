from telethon import TelegramClient, events

from parser import start
from file import read_json

import aiofiles
import json
import asyncio


api_hash = "66272e8ade943a945315ec15220e572b"
api_id = "23564252"
phone_number = "+79869466585"

client = TelegramClient('CheckCitaGetMessages', api_id, api_hash)
start_parser = False

@client.on(events.NewMessage(chats='check_cita_bot')) 
async def handler(event):
    global start_parser
    msg = create_replacer(event.message.text)
    data = await read_json()
    if not start_parser:
        start_parser = True
        print("Парсер успешно запущен")
        await start("parsertest.json", msg)
        start_parser = False
        print("Парсер закончил работу")
    else:
        print("Парсер уже запущен/нет такого сообщения в конфигурационном файле")
    
def create_replacer(message):
    cut_message = message.split("\n")
    return {
        "PROVINCIA": solve[2].split(":")[1][1:],
        "OFICINAS": solve[5][1:],
        "SERVISIO": solve[7][1:]
    }

async def main():
    while True:
        try:
            await client.start(phone_number)
            print("Клиент запущен. Ожидание сообщений от бота...")
            await client.run_until_disconnected() 
        except:
            print("Переподключение через 5 секунд")
            await asyncio.sleep(5)
            print("Переподключаемся...")

with client:
    client.loop.run_until_complete(main())
