import requests


EMPLOYERS = {
    'Яндекс': 1455,
    'Сбер': 3529,
    'VK': 15478,
    'Tinkoff': 78638,
    'Газпром нефть': 67611,
    'Альфа-Банк': 80,
    'Mail.ru': 137,
    'Ozon': 2102,
    'Wildberries': 23427,
    'Лаборатория Касперского': 1740
}

def get_vacancies(employer_id: int) -> list:
    url = f'https://api.hh.ru/vacancies'
    params = {
        'employer_id': employer_id,
        'per_page': 100,
        'page': 0
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get('items', [])
    return []
