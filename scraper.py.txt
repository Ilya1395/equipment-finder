import requests
from bs4 import BeautifulSoup
import re

def search_equipment_specs(code, field1, field2):
    query = f"{code} {field1} {field2} характеристики"
    # Используем DuckDuckGo вместо Google для избежания блокировок
    url = f"https://duckduckgo.com/html/?q={query}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    results = []
    for g in soup.find_all('div', class_='result'):
        link_elem = g.find('a', class_='result__a')
        if link_elem:
            link = link_elem.get('href', '')
            title = link_elem.text
            snippet_elem = g.find('a', class_='result__snippet')
            snippet = snippet_elem.text if snippet_elem else ""
            results.append({"title": title, "snippet": snippet, "link": link})
    return results