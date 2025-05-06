import asyncio
import aiohttp
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# Сюда будем складывать найденные внешние ссылки
external_links = set()

# Проверка на внешнюю ссылку
def is_external(link, base_url):
    base_netloc = urlparse(base_url).netloc
    return urlparse(link).netloc and urlparse(link).netloc != base_netloc

# Асинхронная загрузка страницы
async def fetch(session, url):
    try:
        async with session.get(url, ssl=False) as response:
            return await response.text()
    except Exception as e:
        print(f"Ошибка при загрузке {url}: {e}")
        return ""

# Парсинг и рекурсивный краул
async def crawl(session, url, depth, max_depth, seen):
    if depth > max_depth or url in seen:
        return
    seen.add(url)

    html = await fetch(session, url)
    if not html:
        return

    soup = BeautifulSoup(html, "html.parser")
    for tag in soup.find_all("a", href=True):
        link = urljoin(url, tag["href"])
        if is_external(link, url):
            external_links.add(link)
        else:
            await crawl(session, link, depth + 1, max_depth, seen)

# Главная функция
async def main(start_urls, max_depth=3):
    seen = set()
    async with aiohttp.ClientSession() as session:
        tasks = [crawl(session, url, 0, max_depth, seen) for url in start_urls]
        await asyncio.gather(*tasks)

    # Сохраняем результат
    with open("external_links.txt", "w") as f:
        for link in sorted(external_links):
            f.write(link + "\n")

if __name__ == "__main__":
    urls = ["https://realpython.com/"]
    asyncio.run(main(urls, max_depth=3))