import json
from datetime import datetime
from pathlib import Path
from unittest.mock import Mock, patch

import pandas as pd

from src.reports import spending_by_category


def test_spending_by_category(tmp_path: Path, sample_transactions_to_decorator: pd.DataFrame) -> None:
    # Параметры теста
    search_category = "Супермаркеты"
    date = "01.12.2024"

    # Вызов функции
    result = spending_by_category(sample_transactions_to_decorator, search_category, date)

    # Должно быть 3 операции в категории "Супермаркеты" за последние 3 месяца
    assert len(result) == 3

    # Проверка, что результаты содержат правильные данные
    assert all(result["Категория"] == search_category)


def test_report_write_to_file(tmp_path: Path, sample_transactions_to_decorator: pd.DataFrame) -> None:
    # Параметры теста
    search_category = "Супермаркеты"
    date = "01.12.2024"

    # Вызов функции
    result = spending_by_category(sample_transactions_to_decorator, search_category, date)
    result_dict = result.to_dict(orient="records")

    # Создаем временную директорию

    temp_file = tmp_path / "operation.json"
    temp_file.write_text(json.dumps(result_dict, indent=4))

    assert temp_file.exists()

    with open(temp_file, "r", encoding="utf-8") as file:
        file_content = json.load(file)
        # Преобразуем результат в строку JSON для сравнения
        expected_json = json.dumps(file_content, indent=4, ensure_ascii=False)

        # Убираем пробелы между двоеточием и значением
        expected_json = expected_json.replace(": ", ":")
        file_content_json = json.dumps(file_content, indent=4, ensure_ascii=False).replace(": ", ":")

        # Сравниваем JSON-строки
        assert expected_json == file_content_json


@patch("datetime.datetime")
def test_spending_by_category_without_time(mock_time: Mock, sample_transactions_to_decorator: pd.DataFrame) -> None:
    mock_time.now.return_value = datetime(2024, 12, 12)
    assert len(spending_by_category(sample_transactions_to_decorator, "Супермаркеты")) == 3
