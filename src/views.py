import json

from src.utils import (card_info, filter_transactions_by_date, get_currency_rates, get_greeting, get_stock_prices,
                       read_excel_file, top_five_transactions_by_payment_amount)


def main_page(date: str) -> str:
    """Основная функция для генерации JSON-ответа."""
    greeting = get_greeting()
    data = read_excel_file()
    filter_data = filter_transactions_by_date(data, date)
    card_information = card_info(filter_data)
    top_transactions = top_five_transactions_by_payment_amount(filter_data)
    currency_rates = get_currency_rates()
    stock_prices = get_stock_prices()
    json_data = {
        "greeting": greeting,
        "cards": card_information,
        "top_transactions": top_transactions,
        "currency_rates": currency_rates,
        "stock_prices": stock_prices,
    }
    return json.dumps(json_data, ensure_ascii=False, indent=4)
