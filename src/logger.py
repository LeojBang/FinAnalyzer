import logging
import os
from logging import Logger


def setup_logger(name_module: str, file_name: str) -> Logger:
    # Определяем путь к файлу логов относительно текущего файла
    log_dir = os.path.join(os.path.dirname(__file__), "../logs")
    os.makedirs(log_dir, exist_ok=True)
    log_file_path = os.path.join(log_dir, f"{file_name}.log")

    # Создаем логгер
    logger = logging.getLogger(name_module)
    logger.setLevel(logging.DEBUG)

    # Проверяем, есть ли уже обработчики у логгера
    if not logger.handlers:
        # Создаем обработчик для записи в файл
        file_handler = logging.FileHandler(log_file_path, mode="w", encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)

        # Форматирование логов
        formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
        file_handler.setFormatter(formatter)

        # Добавляем обработчик к логгеру
        logger.addHandler(file_handler)

    return logger
