import psycopg2
from src.config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT

def create_database():
    conn = psycopg2.connect(user=DB_USER, password=DB_PASSWORD,
                            host=DB_HOST, port=DB_PORT)
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(f"DROP DATABASE IF EXISTS {DB_NAME}")
    cur.execute(f"CREATE DATABASE {DB_NAME}")
    cur.close()
    conn.close()

def create_tables():
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER,
                            password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS employers (
            employer_id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS vacancies (
            vacancy_id SERIAL PRIMARY KEY,
            employer_id INT REFERENCES employers(employer_id),
            name VARCHAR(255) NOT NULL,
            salary_from INT,
            salary_to INT,
            currency VARCHAR(10),
            url TEXT
        )
    """)

    conn.commit()
    cur.close()
    conn.close()
