from telethon import TelegramClient, events


api_hash = "0b81f37d6fc6fb66236b1244eda96686"
api_id = "27126498"
phone_number = "2349041793223"

client = TelegramClient('session_name', api_id, api_hash)

@client.on(events.NewMessage(chats='bezrukiitrollvisit')) 
async def handler(event):
    print(f"Новое сообщение от бота: {event.message.text}")

async def main():
    await client.start()
    print("Клиент запущен. Ожидание сообщений от бота...")
    await client.run_until_disconnected() 

with client:
    client.loop.run_until_complete(main())