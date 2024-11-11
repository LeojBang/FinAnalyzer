import datetime
import json
import os
from typing import Any

import pandas as pd
import requests
from dotenv import load_dotenv
from pandas import Series

from src.logger import setup_logger

load_dotenv()
HEADERS = {"apikey": os.getenv("API_KEY_CURRENCY")}
API_KEY_STOCK = os.getenv("API_KEY_STOCK")

default_file_path_to_operations = os.path.join(os.path.dirname(__file__), "../data/operations.xlsx")
file_path_user_settings = os.path.join(os.path.dirname(__file__), "../user_settings.json")

logger = setup_logger("utils", "../logs/utils")


# pypi pytest mock, pytest freezer(time), tmp path, faker(random name example)
def read_excel_file(file_path_operations: str = default_file_path_to_operations) -> pd.DataFrame:
    """Функция принимает путь до EXCEL-файла и возвращает DataFrame"""
    try:
        logger.info(f"Попытка прочтения файла: {file_path_operations[-19::]}")
        operations = pd.read_excel(file_path_operations)
        logger.info("Файл успешно записан в формат DataFrame")
        return operations
    except FileNotFoundError as e:
        logger.error(f"Файл не удалось прочитать. Ошибка: {e.__class__.__name__}")
        raise FileNotFoundError


def filter_transactions_by_date(transactions: pd.DataFrame, date_str: str) -> pd.DataFrame:
    """Функция принимает список словарей с транзакциями и дату
    фильтрует транзакции с начала месяца, на который выпадает входящая дата по входящую дату."""
    logger.info(f"Фильтрую транзакции по дате {date_str}")

    date = datetime.datetime.strptime(date_str, "%d.%m.%Y")

    transactions["Дата операции"] = pd.to_datetime(
        transactions["Дата операции"], format="%d.%m.%Y %H:%M:%S", errors="coerce"
    )
    filtered_operations = transactions.loc[
        (transactions["Дата операции"].dt.month == date.month) & (transactions["Дата операции"].dt.year == date.year)
    ]
    filtered_operations = filtered_operations.copy()
    filtered_operations["Дата операции"] = filtered_operations["Дата операции"].apply(
        lambda x: x.strftime("%d.%m.%Y %H:%M:%S") if pd.notnull(x) else None
    )
    logger.info(f"Фильтрация завершилась успешно. Нашлось {len(filtered_operations)} операций")
    return filtered_operations


def get_greeting() -> str:
    """Функция приветствует в зависимости от времени суток"""
    time_now = datetime.datetime.now().hour
    logger.info(f"Получил время {time_now}. Составляю приветствие...")
    if 6 <= time_now < 12:
        logger.info("Утреннее приветствие сгенерировано")
        return "Доброе утро"
    elif 12 <= time_now < 18:
        logger.info("Дневное приветствие сгенерировано")
        return "Добрый день"
    elif 18 <= time_now < 22:
        logger.info("Вечернее приветствие сгенерировано")
        return "Добрый вечер"
    else:
        logger.info("Ночное приветствие сгенерировано")
        return "Доброй ночи"


def card_info(data: pd.DataFrame) -> list:
    """
    Функция принимает DataFrame.
    Возвращает список словарей из: последние 4 цифры карты, общая сумма расходов, кешбэк (1 рубль на каждые 100 рублей)
    """
    cards = []
    logger.info("Группирую DataFrame по столбцу 'Номер карты'")
    total_spent = data.groupby(by="Номер карты")["Сумма операции"].sum()

    for card_number, spent in total_spent.items():
        last_digits = str(card_number)[-4:]
        cashback = abs(spent // 100)
        cards.append({"last_digits": last_digits, "total_spent": round(spent, 2), "cashback": cashback})

    logger.info(f"Список словарей готов. Нашлось {len(cards)} уникальных карты")
    return cards


def top_five_transactions_by_payment_amount(data: pd.DataFrame) -> list:
    """Функция принимает DataFrame и возвращает топ 5 транзакций в виде списка словарей"""
    logger.info("Составляю топ 5 транзакций по столбцу 'Сумма операции'")

    top_transactions = data.nlargest(5, "Сумма операции")[["Дата операции", "Сумма операции", "Категория", "Описание"]]

    # top_transactions["Дата платежа"] = top_transactions["Дата платежа"].dt.strftime("%d.%m.%Y")
    logger.info("Список словарей из топ 5 транзакций успешно сгенерирован")
    return top_transactions.to_dict(orient="records")


def get_currency_rates() -> dict:
    """Функция возвращает текущий курс валют указанных в файле user.settings.json"""
    with open(f"{file_path_user_settings}", "r") as file:
        json_data = json.load(file)
    logger.info(f"Читаю файл 'user_settings.json'. Буду искать по валютам: {json_data['user_currencies']}")

    url = "https://api.apilayer.com/exchangerates_data/latest?symbols=&base=RUB"
    try:
        logger.info(f"Получаю запрос через API из {url}")
        response = requests.request("GET", url=url, headers=HEADERS)
        response.raise_for_status()

        logger.info(f"Запрос получен. Статус код {response.status_code}")

        return {
            currency: (1 / rate)
            for currency, rate in response.json()["rates"].items()
            if currency in json_data["user_currencies"]
        }
    except requests.exceptions.RequestException as e:
        logger.info(f"Не удалось получить запрос. Ошибка {e.__class__.__name__}")
        return {}


def get_stock_prices() -> list:
    """Функция возвращает текущую стоимость акций указанных в файле user.settings.json"""
    with open(f"{file_path_user_settings}", "r") as file:
        json_data = json.load(file)
    logger.info(f"Читаю файл 'user_settings.json'. Буду искать по акциям: {json_data['user_stocks']}")

    url = f"https://financialmodelingprep.com/api/v3/stock/list?apikey={API_KEY_STOCK}"
    logger.info(f"Получаю запрос через API из {url}")

    r = requests.get(url)
    data_stocks = r.json()
    logger.info(f"Запрос получен. Статус код {r.status_code}")
    stock_prices = [
        {"stock": stock["symbol"], "price": stock["price"]}
        for stock in data_stocks
        if stock["symbol"] in json_data["user_stocks"]
    ]
    logger.info(f"Цены на акции сгенерированы. Количество  {len(stock_prices)}")
    return stock_prices
