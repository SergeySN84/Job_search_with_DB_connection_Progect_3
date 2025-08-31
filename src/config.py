"""
Модуль для загрузки конфигурации из переменных окружения.
"""

import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

# Получаем конфигурационные данные из переменных окружения
DB_NAME: str = os.getenv('DB_NAME', 'hh_vacancies')
DB_USER: str = os.getenv('DB_USER', 'postgres')
DB_PASSWORD: str = os.getenv('DB_PASSWORD', '')
DB_HOST: str = os.getenv('DB_HOST', 'localhost')
DB_PORT: str = os.getenv('DB_PORT', '5432')
