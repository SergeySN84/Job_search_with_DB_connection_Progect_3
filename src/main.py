from src.db_creator import create_database, create_tables
from src.data_loader import save_data_to_db
from src.user_interface import user_menu

def main():
    print("Создание БД и таблиц...")
    create_database()
    create_tables()

    print("Загрузка данных...")
    save_data_to_db()

    print("Данные загружены. Запуск меню...")
    user_menu()

if __name__ == '__main__':
    main()
