import configparser

config = configparser.ConfigParser()  # создаём объекта парсера
config.read("config.ini")  # читаем конфиг
BOT_TOKEN = config["MAIN"]["token"]