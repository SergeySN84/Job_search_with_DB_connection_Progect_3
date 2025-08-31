"""
Модуль для взаимодействия с пользователем через консольный интерфейс.
"""

from typing import List, Tuple, Optional
from .db_manager import DBManager


def display_companies(companies: List[Tuple[str, int]]) -> None:
    """
    Отображает список компаний и количество вакансий.
    """
    print("\nСписок компаний и количество вакансий:")
    print("-" * 50)
    for company, count in companies:
        print(f"{company:<30} {count:>5} вакансий")


def display_vacancies(vacancies: List[Tuple[str, str, Optional[int], Optional[int], str]]) -> None:
    """
    Отображает список вакансий.
    """
    print("\nСписок вакансий:")
    print("-" * 100)
    for company, vacancy, salary_from, salary_to, url in vacancies:
        salary_range = f"{salary_from or 'Не указана'} - {salary_to or 'Не указана'}"
        print(f"Компания: {company}")
        print(f"Вакансия: {vacancy}")
        print(f"Зарплата: {salary_range}")
        print(f"Ссылка: {url}")
        print("-" * 50)


def user_menu() -> None:
    """
    Основное меню взаимодействия с пользователем.
    """
    with DBManager() as db:
        while True:
            print("\n" + "=" * 50)
            print("МЕНЮ ПАРСЕРА ВАКАНСИЙ")
            print("=" * 50)
            print("1. Список компаний и количество вакансий")
            print("2. Все вакансии")
            print("3. Средняя зарплата")
            print("4. Вакансии с зарплатой выше средней")
            print("5. Поиск вакансий по ключевому слову")
            print("0. Выход")
            print("=" * 50)

            choice = input("Выберите действие (0-5): ").strip()

            if choice == '1':
                companies = db.get_companies_and_vacancies_count()
                display_companies(companies)

            elif choice == '2':
                vacancies = db.get_all_vacancies()
                display_vacancies(vacancies[:10])  # Показываем первые 10 вакансий
                if len(vacancies) > 10:
                    print(f"\nПоказаны первые 10 из {len(vacancies)} вакансий")

            elif choice == '3':
                avg_salary = db.get_avg_salary()
                print(f"\nСредняя зарплата по всем вакансиям: {avg_salary:.2f} руб.")

            elif choice == '4':
                high_salary_vacancies = db.get_vacancies_with_higher_salary()
                print(f"\nВакансии с зарплатой выше средней ({db.get_avg_salary():.2f} руб.):")
                display_vacancies(high_salary_vacancies[:10])  # Показываем первые 10
                if len(high_salary_vacancies) > 10:
                    print(f"\nПоказаны первые 10 из {len(high_salary_vacancies)} вакансий")

            elif choice == '5':
                keyword = input("Введите ключевое слово для поиска: ").strip()
                if keyword:
                    keyword_vacancies = db.get_vacancies_with_keyword(keyword)
                    if keyword_vacancies:
                        print(f"\nВакансии, содержащие '{keyword}':")
                        display_vacancies(keyword_vacancies)
                    else:
                        print(f"Вакансии с ключевым словом '{keyword}' не найдены")
                else:
                    print("Ключевое слово не может быть пустым")

            elif choice == '0':
                print("Спасибо за использование парсера вакансий!")
                break

            else:
                print("Неверный выбор. Пожалуйста, выберите число от 0 до 5.")


if __name__ == '__main__':
    user_menu()
