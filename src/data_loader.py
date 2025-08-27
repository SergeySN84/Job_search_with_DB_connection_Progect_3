import psycopg2
from src.hh_api import EMPLOYERS, get_vacancies
from src.config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT

def save_data_to_db():
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER,
                            password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    cur = conn.cursor()

    for name, employer_id in EMPLOYERS.items():
        cur.execute("INSERT INTO employers (name) VALUES"
                    " (%s) RETURNING employer_id", (name,))
        emp_id = cur.fetchone()[0]

        vacancies = get_vacancies(employer_id)
        for vac in vacancies:
            salary = vac.get('salary')
            salary_from = salary.get('from') if salary else None
            salary_to = salary.get('to') if salary else None
            currency = salary.get('currency') if salary else None

            cur.execute("""
                INSERT INTO vacancies (employer_id, name,
                 salary_from, salary_to, currency, url)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (emp_id, vac['name'], salary_from,
                  salary_to, currency, vac['alternate_url']))

    conn.commit()
    cur.close()
    conn.close()
