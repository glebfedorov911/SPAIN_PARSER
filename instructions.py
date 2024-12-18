{
    "0": 
    {
        "0": ["Запустить парсер", "https://sede.administracionespublicas.gob.es/pagina/index/directorio/icpplus"],
        "1": ["Нажать кнопку", ".uppercase.button_next"],
        "2": ["Выбрать значение", "Valencia", "#form"],
        "3": ["Нажать кнопку", "#btnAceptar"],
        "4": ["Выбрать значение", "CNP COMISARIA DE BURJASOT, C/  Doctor Joan Pesset , 2, Burjassot", "#sede", "optgroup"],
        "5": ["Выбрать значение", "POLICIA-CARTA DE INVITACIÓN", ".mf-input__l", ".mf-input__l"],
        "6": ["Нажать кнопку", "#btnAceptar"],
        "7": ["Нажать кнопку", "#btnAccesoClave"],
        "8": ["Альтернативное нажатие", "JAVASCRIPT:selectedIdP('AFIRMA');idpRedirect.submit();"],
        "9": ["Нажать enter", "2"],
        "10": ["Нажать кнопку", "#rdbTipoDocNie"],
        "11": ["Заполнить поле", ["Y5008755J", "Y5008703F"], "#txtIdCitado"],
        "12": ["Заполнить поле", ["DANIL RUBIN", "VITALII PANFILOV"], "#txtDesCitado"],
        "13": ["Нажать кнопку", "#btnEnviar"],
        "14": ["Нажать кнопку", "#btnEnviar"],
        "15": ["Заполнить поле", "612345658", ".cajapeque"],
        "16": ["Заполнить поле", "612345658a@gmail.com", "#emailUNO"],
        "17": ["Заполнить поле", "612345658a@gmail.com", "#emailDOS"],
        "18": ["Нажать кнопку", "#btnSiguiente"],
        "19": ["Нажать кнопку", "#cita1"],
        "20": ["Записать дату", "cita1", "Record"],
        "21": ["Нажать кнопку", "#btnSiguiente"],
        "22": ["Нажать кнопку", "body > div.jconfirm.jconfirm-light.jconfirm-open > div.jconfirm-scrollpane > div > div > div > div > div > div > div > div.jconfirm-buttons > button:nth-child(1)"],
        "23": ["Нажать кнопку", "#chkTotal"],
        "24": ["Нажать кнопку", "#enviarCorreo"],
        "25": ["Альтернативное нажатие", "envia()"],
        "26": ["Нажать кнопку", "#btnSalir"]
    }
}

'''
ИНСТРУКЦИЯ

Для того чтобы запустить интеграция с телеграмм, то нужно запустить файл tg.py и ввести данные
Перед тем, как активировать интеграцию необходимо заполнить файл file_service.json, после каждого его изменения - перезапускаем интеграцию
file_service.json принимает ключ и значение, где ключ - сообщение от телеграмм бота, а значение - название файла который нужно спарсить.

В случае, если нам не нужен тг, но нужно запустить программу, то нужно запустить файл parser.py (ПЕРЕД ЭТИМ ВЫКЛЮЧИТЬ ПРОГРАММУ, ЕСЛИ ОНА БЫЛА ЗАПУЩЕНА/БЫЛ ЗАПУЩЕН ТГ)
в parser.py нужно заменить значение в переменной filename на название файла, в котором прописан текущий конструктор (выше пример конструктора)

ФУНКЦИИ КОНСТРУКТОРА И АРГУМЕНТЫ ФУНКЦИЙ
    Конструктор (в скобках пример индексов):
    
    -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    {
        "индекс браузера (1)":
        {
            "индекс функции (1)": ["КОМАНДА", "АР", "ГУ", "МЕН", "ТЫ"]
            "индекс функции (2)": ["КОМАНДА", "АР", "ГУ", "МЕН", "ТЫ"]
            "индекс функции (3)": ["КОМАНДА", "АР", "ГУ", "МЕН", "ТЫ"]
            "индекс функции (4)": ["КОМАНДА", "АР", "ГУ", "МЕН", "ТЫ"]
        },
        "индекс браузера (2)":
        {
            "индекс функции (1)": ["КОМАНДА", "АР", "ГУ", "МЕН", "ТЫ"]
            "индекс функции (2)": ["КОМАНДА", "АР", "ГУ", "МЕН", "ТЫ"]
            "индекс функции (3)": ["КОМАНДА", "АР", "ГУ", "МЕН", "ТЫ"]
            "индекс функции (4)": ["КОМАНДА", "АР", "ГУ", "МЕН", "ТЫ"]
        }
    }
    -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

    !!!ВНИМАНИЕ!!! cелекторы с [] не принимаются!!! Пример: #idNekotoryi[1], лучше выбрать class и обозначить какой он по счету, где это возможно (idx) - читать ниже

    1) Запустить парсер -> ["Запустить парсер", "url"]
        • url - ссылка на которую перейдет парсер при запуске (указывается первая страница сайта)
    2) Нажать кнопку -> ["Нажать кнопку", "selector", "idx"]
        • selector - селектор кнопки, смотрим его в DevTools(F12 на сайте) - выбираем между class и id (приоритет id), если выбрали id, то перед селектором пишем #
        если выбрали class, то перед селектором пишем . Примеры: (.cajapeque - id | #btnSiguiente - class)
        • idx - если у нескольких кнопок одинаковые id/class, то мы можем указать ее порядковый номер (от 1 до N, где N - количество кнопок на странице)
    3) Выбрать значение -> ["Выбрать значение",  "option_value", "form_selector", "option_selector", "idx"] ---- выпадающий список
        • option_value - значение, которые мы хотим выбрать (в точности как на сайте, можно через DevTools посмотреть)
        • form_selector - селектор, в котором находятся все options (например в тэгах <form> или <select>, также указываем id или class)
        • option_selector - необязательный параметр, если на странице 2 и более options, то его нужно указать (либо селектор id или class, либо optgroup (приоритетнее Optgroup))
        • idx - выбрать поле (если у него одинаковый селектор), по порядку (с 1 до N), где N - количество форм с ОДИНАКОВЫМ селектором
    4) Альтернативное нажатие -> ["Альтернативное нажатие", "eval"]
        • eval - значение, которое указывается в атрибутах тэга, атрибуты: onclick="" или onsubmit="", 
        пример: ["Альтернативное нажатие", "JAVASCRIPT:selectedIdP('AFIRMA');idpRedirect.submit();"] 
    5) Нажать enter -> ["Нажать enter", "number"] - Используется если используем ЭПЦ (тк есть необходимость выбрать подпись)
        • number - выбор какая ЭПЦ по счету нужна (с 1 и до N), где N - количество ЭПЦ
    6) Заполнить поле -> ["Заполнить поле", "value_for_fill", "selector"] ---- форма ввода
        • value_for_fill - значением, которым мы хотим заполнить форму
        !!!ВНИМАНИЕ!!! value_for_fill, если нужно выбрать только одно значение (не изменять его при перезапуске программы), то пишем просто в кавычках значение
        если нужно по ходу программы чтобы оно изменялось(например при первом запуске браузера используем первый элемент, при втором второй, при третьем первый и так далее),
        то указывает в [], пример "11": ["Заполнить поле", ["Y5008755J", "Y5008703F"], "#txtIdCitado"],
        пример без [] "11": ["Заполнить поле", "Y5008755J", "#txtIdCitado"], 
        (ЗДЕСЬ УКАЗАНЫ ЗНАЧЕНИЯ ДЛЯ ПРИМЕРА, МОЖНО ИЗМЕНЯТЬ ТАКЖЕ ПОЧТУ И НОМЕР)
        • selector - class или id
    7) Прислать уведомление -> ["Прислать уведомление", "time_to_finish"]
        • time_to_finish - время, которое парсер будет бездействовать, само уведомление длится 1.5 секунд (звуковой сигнал), после него парсер не будет продолжать работа
        time_to_finish секунд (изначальное значение - 2 секунды), поле не является обязательным
        Пример использования, если нам нужно ввести СМС-код (если мы не используем ЭПЦ) мы можем прислать уведомление и поставить таймаут 20 секунд, время за которое введем смс
    8) Поставить задержку -> ["Поставить задержку", "time"]
        • time - время, которое парсер будет бездействовать, поле является обязательным
        Пример использования, если мы не знаем селектор (id или class) какого-то из полей, то можем поставить задержку и посмотреть, далее перезапустить парсер
    9) Записать дату -> ["Записать дату", "selector", "name"]
        • selector - правой кнопкой нажать по элементу - copy > copy selector
        Используется при записи данных, на какое время взята запись, обычно указывается тоже что и в выборе записи
        Пример:
        "19": ["Нажать кнопку", "#cita1"],
        "20": ["Записать дату", "cita1", "Number1"],
        • name - то, под каким именем сохраниться в файле records/record.txt значение записи
        Пример: {'Number1': 'CITA 1 Día: 05/11/2024 Hora: 18:40 '} ---- Number1 - name
    10) Решить капчу -> ["Решить капчу"] ---- Если на странице ожидается капча, то указывается это поле (например, после выбора записи)
'''