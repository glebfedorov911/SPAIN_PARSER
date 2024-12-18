import asyncio

from ParserConstuctor import ParserConstructor

finished = []

async def parser_worker(delay: int, n: int, queue: asyncio.Queue, msg=None):
    global finished
    finished = []
    print(f"до запуска {n} воркера осталось {delay} секунд")
    await asyncio.sleep(delay=delay)
    number_of_validate_data = 0
    while True:
        print("Цикл запущен")
        host, port, login, password, worker_data, index_finish = await queue.get()
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
            "Решить капчу": pc.solve_captchas,
        }

        try:
            for index_page_data in worker_data:
                if index_finish in finished:
                    print("Завершил досрочно")
                    await pc.finish()
                    break
                data = worker_data[index_page_data]
                args = data[1:]
                if data[0] in commands:
                    arguments = list(args)
                    information = arguments[0].split("_")
                    if len(information) >= 2 and information[1] == "PLACE":
                        arguments[0] = msg[information[0]]
                    if data[0] == "Заполнить поле" or data[0] == "Записать дату":
                        if number_of_validate_data >= len(args[0]):
                            number_of_validate_data = 0
                        arguments.append(number_of_validate_data)
                    await commands[data[0]](*arguments)
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
            number_of_validate_data += 1
            queue.task_done()
            finished.append(index_finish)