import datetime
import math
from typing import Any, Hashable

from src.logger import setup_logger
from src.utils import read_excel_file

transactions = read_excel_file()

logger = setup_logger("services")


def investment_bank(month: str, transactions: list[dict[Hashable, Any]], limit: int) -> float:
    """На вход принимаем месяц, транзакции, кратная сумма, до которой округляем.
    Каждая покупка округляется до кратной суммы"""
    date = datetime.datetime.strptime(month, "%Y-%m")
    logger.info(f"Запускаю расчет инвесткопилки для месяца {datetime.datetime.strftime(date, "%B")} с лимитом {limit}")
    sum_investment_bank = 0.0

    for transaction in transactions:
        transaction_date_to_datetime = datetime.datetime.strptime(transaction["Дата операции"], "%d.%m.%Y %H:%M:%S")

        if transaction_date_to_datetime.month == date.month and transaction_date_to_datetime.year == date.year:
            payment = transaction["Сумма платежа"]

            if payment < 0 and transaction["Категория"] != "Переводы" and transaction["Категория"] != "Наличные":

                rounded_payment = math.ceil(payment / limit) * limit
                sum_investment_bank += round(abs(rounded_payment - payment), 1)

    logger.info(
        f"Готово. Сумма накоплений за {datetime.datetime.strftime(date, "%B")} месяц составила {sum_investment_bank}"
    )

    return sum_investment_bank
