import re
import json
import requests
from bs4 import BeautifulSoup


def find_last_content(block):
    if "content" in block and block["content"] == []:
        return block
    elif "content" in block:
        for item in block["content"]:
            result = find_last_content(item)
            print('rec', result)
            if result:
                return result
    return None


def get_internship_data(data):
    """
    Анализирует JSON и возвращает список направлений стажировок с информацией.

    Args:
        data: Словарь, содержащий JSON данные.

    Returns:
        Список словарей, где каждый словарь представляет одно направление
        стажировки с информацией о названии, месте проведения и статусе набора.
    """
    content_config = data["stores"]["router"]["currentRoute"]["config"]["content"]["content"]
    internships = list()
    print(content_config)
    for item in content_config:
        result = find_last_content(item)
        # print(item)
        if result and result["type"] == "mobilePanelsSlider":
            internships.append(result)
        else:
            continue
    return internships

    # Ищем блок с названием "mobileTabsContainer"
    # for _ in content_config:
    #     for block in content_config.values() if isinstance(content_config, dict) else content_config:
    #         print(block)
    #         for item in block:
    #             print(item)
    #             if item["type"] == "mobilePanelsSlider":
    #                 tabs_data = item["content"]
    #                 break
    #         else:
    #             return []  # Если блок не найден, возвращаем пустой список

    # internships = []
    # # Перебираем вкладки (аналитика, разработка, дизайн, QA, менеджмент)
    # for tab in tabs_data:
    #     # Внутри каждой вкладки находим "mobilePanelsSlider"
    #     for panel_slider in tab["content"]:
    #         if panel_slider["type"] == "mobilePanelsSlider":
    #             # Внутри слайдера перебираем карточки направлений
    #             for panel in panel_slider["properties"]["panelList"]:
    #                 title_text = panel["title"]["text"]
    #                 # Извлекаем место проведения из текста заголовка
    #                 location = title_text.split("<div class=\"text_2\">")[1].split("</span>")[0]
    #                 # Извлекаем название направления
    #                 name = title_text.split("<div class=\"header_2\">")[1].split("</div>")[0]
    #                 # Извлекаем статус набора
    #                 status = panel["subtitle"]["text"].split("<p>")[1].split("</span>")[0]
    #                 internships.append({
    #                     "name": name,
    #                     "location": location,
    #                     "status": status,
    #                     "url": panel["slideLink"]["url"]
    #                 })


def parse_tinkoff_internships():
    url = 'https://fintech.tinkoff.ru/start/'
    response = requests.get(url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')

    internships = []

    # Найти скрипт с id="__TRAMVAI_STATE__"
    script = soup.find('script', {'id': '__TRAMVAI_STATE__'})

    if script:
        # Извлечь содержимое скрипта
        json_data = script.string

        # Распарсить JSON
        data = json.loads(json_data)
        with open('tinkoff.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        # Получить массив блоков контента
        content_blocks = data['stores']['actionTramvai']['serverState']['content']

        # Пройтись по блокам и найти блоки со стажировками
        for block in content_blocks:
            if block['type'] == 'desktopTab':
                internship_blocks = block['content']

                for internship_block in internship_blocks:
                    if internship_block['type'] == 'desktopTextPanels':
                        for panel in internship_block['panels']:
                            title = panel['title']
                            description = panel['subtitle']
                            status = panel['badges'][0]['title'] if panel['badges'] else ''

                            internship = {
                                'title': title,
                                'description': description,
                                'status': status
                            }
                            internships.append(internship)

    return internships


if __name__ == '__main__':

    with open('../tinkoff.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Пример использования
    internships_json = get_internship_data(data)
    print(internships_json)

    internships = []

    for item in internships_json:
        if item['type'] == 'mobilePanelsSlider':
            text = item['properties']['panelList']
            for block in text:
                title = block['title']['text']
                description = block['subtitle']['text']
                status = block['subtitle']['text']
                internship = {
                    'title': title,
                    'description': description,
                    'status': status
                }
                internships.append(internship)

    print(internships)
    # for internship in internships:
    #     print(f"Название: {internship['name']}")
    #     print(f"Место проведения: {internship['location']}")
    #     print(f"Статус набора: {internship['status']}")
    #     print(f"Ссылка: https://fintech.tinkoff.ru{internship['url']}")
    #     print("-----")
