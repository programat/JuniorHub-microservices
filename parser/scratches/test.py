import json


def extract_mobile_panels_slider(data):
    results = []

    def recurse_items(items):
        if isinstance(items, dict):
            if items.get('type') == 'mobilePanelsSlider':
                results.append(items)
            for key, value in items.items():
                if isinstance(value, (dict, list)):
                    recurse_items(value)
        elif isinstance(items, list):
            for item in items:
                recurse_items(item)

    recurse_items(data)
    return results

# Загрузка данных из файла
with open("../../tinkoff.json", "r", encoding="utf-8") as file:
    json_data = json.load(file)

# Извлечение данных и сохранение результатов в массив
mobile_panels_sliders = extract_mobile_panels_slider(json_data)
# print(mobile_panels_sliders)

# Вывод результатов
for slider in mobile_panels_sliders:
    print(slider)
