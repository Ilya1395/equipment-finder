import re
import pandas as pd
from transformers import pipeline

# Используем лёгкую модель для распознавания именованных сущностей
model_name = "cointegrated/rubert-tiny2"

try:
    nlp = pipeline(
        "ner",
        model=model_name,
        aggregation_strategy="simple"
    )
except Exception as e:
    print(f"Ошибка загрузки модели: {e}")
    nlp = None

# Словарь единиц измерения и их сокращений
UNITS_DICT = {
    'киловатт': 'кВт', 'ватт': 'Вт', 'мегаватт': 'МВт',
    'килограмм': 'кг', 'грамм': 'г', 'тонна': 'т',
    'метр': 'м', 'километр': 'км', 'сантиметр': 'см', 'миллиметр': 'мм',
    'литр': 'л', 'кубический метр': 'м³', 'кубометр': 'м³',
    'час': 'ч', 'минута': 'мин', 'секунда': 'с',
    'ампер': 'А', 'вольт': 'В', 'ом': 'Ом',
    'кубометров в час': 'м³/ч', 'литров в минуту': 'л/мин',
    'метров кубических в час': 'м³/ч'
}

def normalize_unit(unit_text):
    """Нормализует единицы измерения к сокращённому виду СИ"""
    unit_text = unit_text.lower().strip()
    for full_name, short_name in UNITS_DICT.items():
        if full_name in unit_text:
            return short_name
    return unit_text

def extract_specs_with_ai(raw_data, code, field1, field2):
    data = []
    # Регулярное выражение для поиска характеристик: название: значение единица
    pattern = r'([А-Яа-яA-Za-z\s]{3,}?)\s*[:–-]\s*([\d,]+(?:\.\d+)?)\s*([А-Яа-яa-zA-Z\s]{1,15}?)(?:\.|\s|$)'

    for item in raw_data:
        text = item["title"] + " " + item["snippet"]
        matches = re.findall(pattern, text, re.IGNORECASE)

        for name, value, unit in matches:
            # Очищаем название характеристики
            name = re.sub(r'[^А-Яа-яA-Za-z\s]', '', name).strip()
            if len(name) < 2:  # Пропускаем слишком короткие названия
                continue

            # Нормализуем единицу измерения
            normalized_unit = normalize_unit(unit)

            data.append({
                "Поле №1": field1,
                "Поле №2": field2,
                "Код": code,
                "Характеристика": name,
                "Значение": value.replace(',', '.'),  # Заменяем запятую на точку для десятичных
                "Единица измерения": normalized_unit
            })

    return pd.DataFrame(data)
