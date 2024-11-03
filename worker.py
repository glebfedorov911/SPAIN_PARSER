import asyncio

from ParserConstuctor import ParserConstructor


async def parser_worker(queue: asyncio.Queue):
    atms = 0
    while True:
        print("Цикл запущен")
        host, port, login, password, worker_data = await queue.get()
        pc = ParserConstructor(host=host, port=port, login=login, password=password)

        commands = {
            "Запустить парсер": pc.start,
            "Нажать кнопку": pc.button_click,
            "Выбрать значение": pc.select_option,
            "Альтернативное нажатие": pc.alternative_for_next_page,
            "Нажать enter": pc.click_enter_on_page,
            "Заполнить поле": pc.fill_field,
            "Прислать уведомление": pc.notification,
            "Записать дату": pc.save_time_record,
            "Поставить задержку": pc.waiting,
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
            atms += 1
            print("Ошибка в основном цикле", e if e else '')
            print("Добавляем обратно в очередь")
            if atms < 7:
                print(atms)
                await queue.put((host, port, login, password, worker_data))
            else:
                print("Попытки закончились, браузер закрывается навсегда и уже не откроется.")
            await pc.finish()
        finally:
            queue.task_done()