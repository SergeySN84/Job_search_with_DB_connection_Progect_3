from src.db_manager import DBManager

def user_menu():
    db = DBManager()
    while True:
        print("\n1. Список компаний и количество вакансий")
        print("2. Все вакансии")
        print("3. Средняя зарплата")
        print("4. Вакансии с зарплатой выше средней")
        print("5. Поиск вакансий по ключевому слову")
        print("0. Выход")

        choice = input("Выберите действие: ")

        if choice == '1':
            for row in db.get_companies_and_vacancies_count():
                print(f"{row[0]} — {row[1]} вакансий")
        elif choice == '2':
            for row in db.get_all_vacancies():
                print(f"{row[0]} — {row[1]} | ЗП: {row[2]}–{row[3]} {row[4]}")
        elif choice == '3':
            print(f"Средняя зарплата: {db.get_avg_salary()} руб.")
        elif choice == '4':
            for row in db.get_vacancies_with_higher_salary():
                print(f"{row[0]} — {row[1]} | ЗП: {row[2]}–{row[3]} {row[4]}")
        elif choice == '5':
            keyword = input("Введите ключевое слово: ")
            for row in db.get_vacancies_with_keyword(keyword):
                print(f"{row[0]} — {row[1]} | ЗП: {row[2]}–{row[3]} {row[4]}")
        elif choice == '0':
            db.close()
            break
        else:
            print("Неверный выбор.")
