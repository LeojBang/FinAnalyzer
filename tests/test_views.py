import json
from unittest.mock import patch

from src.views import main_page


def test_main_page(expected_result: dict) -> None:
    # Патчим функции, которые вызываются внутри main_page
    with patch("src.views.get_greeting", return_value="Доброй ночи"), patch(
        "src.views.read_excel_file", return_value=[]
    ), patch("src.views.filter_transactions_by_date", return_value=[]), patch(
        "src.views.card_info", return_value=expected_result["cards"]
    ), patch(
        "src.views.top_five_transactions_by_payment_amount", return_value=expected_result["top_transactions"]
    ), patch(
        "src.views.get_currency_rates", return_value=expected_result["currency_rates"]
    ), patch(
        "src.views.get_stock_prices", return_value=expected_result["stock_prices"]
    ):

        # Запуск тестируемой функции
        result = main_page("31.12.2021")

        # Проверка того, что возвращаемое значение соответствует ожидаемому
        expected_json = json.dumps(expected_result, ensure_ascii=False, indent=4)
        assert result == expected_json
