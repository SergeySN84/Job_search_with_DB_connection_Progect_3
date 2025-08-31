"""
Класс для работы с базой данных PostgreSQL.

Реализует методы для получения информации о компаниях и вакансиях.
"""

import psycopg2
from typing import Tuple, Optional, Any
from .config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT


class DBManager:
    """
    Класс для работы с базой данных PostgreSQL.

    Предоставляет методы для получения информации о компаниях и вакансиях
    через SQL-запросы к базе данных.
    """

    def __init__(self) -> None:
        """
        Инициализация подключения к базе данных.
        """
        try:
            self.conn = psycopg2.connect(
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD,
                host=DB_HOST,
                port=DB_PORT
            )
            self.cur = self.conn.cursor()
        except psycopg2.Error as e:
            raise psycopg2.Error(f"Не удалось подключиться к базе данных: {e}")

    def get_companies_and_vacancies_count(self) -> Any[Tuple[str, int]]:
        """
        Получает список всех компаний и количество вакансий у каждой компании.

        Использует SQL-запрос с JOIN для объединения таблиц employers и vacancies.
        """
        self.cur.execute("""
            SELECT e.name, COUNT(v.vacancy_id) as vacancy_count
            FROM employers e
            LEFT JOIN vacancies v ON e.employer_id = v.employer_id
            GROUP BY e.employer_id, e.name
            ORDER BY vacancy_count DESC
        """)
        return self.cur.fetchall()

    def get_all_vacancies(self) -> Any[Tuple[str, str, Optional[int], Optional[int], str]]:
        """
        Получает список всех вакансий с указанием названия компании,
        названия вакансии, зарплаты и ссылки на вакансию.

        Использует SQL-запрос с JOIN для объединения информации из двух таблиц.
        """
        self.cur.execute("""
            SELECT e.name, v.name, v.salary_from, v.salary_to, v.url
            FROM vacancies v
            JOIN employers e ON v.employer_id = e.employer_id
            ORDER BY e.name, v.name
        """)
        return self.cur.fetchall()

    def get_avg_salary(self) -> float:
        """
        Получает среднюю зарплату по всем вакансиям.

        Использует SQL-функцию AVG для расчета среднего значения.
        Учитываются только вакансии с указанной зарплатой (от и до).
        """
        self.cur.execute("""
            SELECT AVG((salary_from + salary_to) / 2.0) as avg_salary
            FROM vacancies
            WHERE salary_from IS NOT NULL AND salary_to IS NOT NULL
        """)
        result = self.cur.fetchone()[0]
        return round(result, 2) if result else 0.0

    def get_vacancies_with_higher_salary(self) -> Any[Tuple[str, str, Optional[int], Optional[int], str]]:
        """
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        Использует подзапрос и фильтрацию WHERE для сравнения с средней зарплатой.
        """
        self.cur.execute("""
            SELECT e.name, v.name, v.salary_from, v.salary_to, v.url
            FROM vacancies v
            JOIN employers e ON v.employer_id = e.employer_id
            WHERE (v.salary_from + v.salary_to) / 2.0 > (
                SELECT AVG((salary_from + salary_to) / 2.0)
                FROM vacancies
                WHERE salary_from IS NOT NULL AND salary_to IS NOT NULL
            )
            ORDER BY (v.salary_from + v.salary_to) / 2.0 DESC
        """)
        return self.cur.fetchall()

    def get_vacancies_with_keyword(self, keyword: str) -> Any[Tuple[str, str, Optional[int], Optional[int], str]]:
        """
        Получает список всех вакансий, в названии которых содержатся переданные слова.

        Использует оператор LIKE для поиска по ключевому слову (регистронезависимый поиск).
        """
        self.cur.execute("""
            SELECT e.name, v.name, v.salary_from, v.salary_to, v.url
            FROM vacancies v
            JOIN employers e ON v.employer_id = e.employer_id
            WHERE LOWER(v.name) LIKE LOWER(%s)
            ORDER BY e.name, v.name
        """, (f'%{keyword}%',))
        return self.cur.fetchall()

    def close(self) -> None:
        """
        Закрывает соединение с базой данных.

        Всегда вызывайте этот метод после завершения работы с базой данных
        или используйте контекстный менеджер.
        """
        if hasattr(self, 'cur') and self.cur:
            self.cur.close()
        if hasattr(self, 'conn') and self.conn:
            self.conn.close()

    def __enter__(self) -> 'DBManager':
        """
        Контекстный менеджер для автоматического закрытия соединения.
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Автоматическое закрытие соединения при выходе из контекста.
        """
        self.close()
