import psycopg2
from src.config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT


class DBManager:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        self.cur = self.conn.cursor()

    def get_companies_and_vacancies_count(self):
        self.cur.execute("""
            SELECT e.name, COUNT(v.vacancy_id)
            FROM employers e
            JOIN vacancies v ON e.employer_id = v.employer_id
            GROUP BY e.name
        """)
        return self.cur.fetchall()

    def get_all_vacancies(self):
        self.cur.execute("""
            SELECT e.name, v.name, v.salary_from, v.salary_to, v.url
            FROM vacancies v
            JOIN employers e ON v.employer_id = e.employer_id
        """)
        return self.cur.fetchall()

    def get_avg_salary(self):
        self.cur.execute("""
            SELECT AVG((salary_from + salary_to) / 2)
            FROM vacancies
            WHERE salary_from IS NOT NULL AND salary_to IS NOT NULL
        """)
        result = self.cur.fetchone()[0]
        return round(result, 2) if result else 0

    def get_vacancies_with_higher_salary(self):
        avg = self.get_avg_salary()
        self.cur.execute("""
            SELECT e.name, v.name, v.salary_from, v.salary_to, v.url
            FROM vacancies v
            JOIN employers e ON v.employer_id = e.employer_id
            WHERE (v.salary_from + v.salary_to) / 2 > %s
        """, (avg,))
        return self.cur.fetchall()

    def get_vacancies_with_keyword(self, keyword: str):
        self.cur.execute("""
            SELECT e.name, v.name, v.salary_from, v.salary_to, v.url
            FROM vacancies v
            JOIN employers e ON v.employer_id = e.employer_id
            WHERE LOWER(v.name) LIKE %s
        """, (f'%{keyword.lower()}%',))
        return self.cur.fetchall()

    def close(self):
        self.cur.close()
        self.conn.close()
