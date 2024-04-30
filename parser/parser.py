import re
import json
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://fintech.tinkoff.ru"


def extract_text(text, pattern):
    """Извлекает текст из строки по заданному шаблону."""
    match = re.search(pattern, text, re.DOTALL)
    return match.group(1).strip() if match else ""


def parse_position(panel):
    """Парсит информацию о вакансии из панели."""
    soup = BeautifulSoup(panel['title']['text'], 'html.parser')
    full_text = soup.get_text(strip=True)

    # Извлекаем area и title, учитывая возможность отсутствия area
    div_text = soup.find('div', class_='text_2')
    if div_text:
        area = div_text.get_text(strip=True)
        title = full_text.replace(area, "").strip()
    else:
        area = ""
        title = full_text

    # Извлекаем description, удаляя HTML теги
    description_soup = BeautifulSoup(panel['subtitle']['text'], 'html.parser')
    description = description_soup.find('p').get_text(separator=' ', strip=True)

    status = extract_text(panel['subtitle']['text'], r'background-color:;">(.+?)</span>')
    link = BASE_URL + panel['slideLink']['url']
    return {
        "title": title,
        "description": description,
        "status": status,
        "link": link,
        "area": area
    }


def parse_category(tab):
    """Парсит информацию о категории стажировок из вкладки."""
    category = tab['properties']['name']['text']
    positions = [parse_position(panel) for panel in tab['content'][0]['properties']['panelList']]
    return {
        "category": category,
        "positions": positions
    }


def parse_internships(data):
    """Парсит список данных и преобразует его в нужный формат."""
    internships = [parse_category(tab) for tab in data]
    return {"internships": internships}


def extract_mobile_panels_slider(data):
    """Извлекает данные из блока mobilePanelsSlider."""
    results = []

    def recurse_items(items, parent=None):
        if isinstance(items, dict):
            if items.get('type') == 'mobilePanelsSlider':
                results.append(parent)
            for key, value in items.items():
                if isinstance(value, (dict, list)):
                    recurse_items(value, items)
        elif isinstance(items, list):
            for item in items:
                recurse_items(item, parent)

    recurse_items(data)
    return results


def parse_tinkoff_internships():
    """
    Парсит стажировки с сайта Тинькофф и возвращает результат в формате JSON.
    """
    url = 'https://fintech.tinkoff.ru/start/'
    response = requests.get(url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')

    # Найти скрипт с id="__TRAMVAI_STATE__"
    script = soup.find('script', {'id': '__TRAMVAI_STATE__'})
    if not script:
        return None  # Обработка случая, если скрипт не найден

    # Извлечь содержимое скрипта и распарсить JSON
    json_data = json.loads(script.string)

    # Извлечь данные из нужного блока
    mobile_panels_sliders = extract_mobile_panels_slider(json_data)
    with open("tinkoff_internships.json", "w", encoding="utf-8") as f:
        json.dump(mobile_panels_sliders, f, ensure_ascii=False, indent=4)

    # Парсинг стажировок
    result = parse_internships(mobile_panels_sliders)
    return result


if __name__ == '__main__':
    # Загрузка данных из файла
    with open("../tinkoff.json", "r", encoding="utf-8") as file:
        json_data = json.load(file)
