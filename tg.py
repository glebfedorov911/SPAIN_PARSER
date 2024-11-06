from telethon import TelegramClient, events

from parser import start
from file import read_json

import aiofiles
import json
import asyncio


api_hash = "66272e8ade943a945315ec15220e572b"
api_id = "23564252"
phone_number = "+79869466585"

client = TelegramClient('WorkWithTg', api_id, api_hash)
start_parser = False

@client.on(events.NewMessage(chats='check_cita_bot')) 
async def handler(event):
    global start_parser
    msg = event.message.text
    data = await read_json()
    if msg in data and not start_parser:
        start_parser = True
        print("Парсер успешно запущен")
        await start(data[msg])
        start_parser = False
        print("Парсер закончил работу")
    else:
        print("Парсер уже запущен/нет такого сообщения в конфигурационном файле")
        

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
