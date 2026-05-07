import requests
from bs4 import BeautifulSoup → from bs4 import BeautifulSoup
import re

def search_equipment_specs(code, field1, field2):
    query = f"{code} {field1} {field2} характеристики"
    # Используем DuckDuckGo вместо Google для избежания блокировок
    url = f"https://duckduckgo.com/html/?q={query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Проверяем статус ответа
    except requests.RequestException as e:
        print(f"Ошибка запроса: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    results = []

    # Ищем блоки результатов поиска
    for g in soup.find_all('div', class_='result'):
        link_elem = g.find('a', class_='result__a')
        if link_elem:
            link = link_elem.get('href', '')
            title = link_elem.text
            snippet_elem = g.find('a', class_='result__snippet')
            snippet = snippet_elem.text if snippet_elem else ""
            results.append({
                "title": title,
                "snippet": snippet,
                "link": link
            })
    return results
