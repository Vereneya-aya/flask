import asyncio
import aiohttp

# Синхронная функция для записи файла
def write_file(path, data):
    with open(path, "wb") as f:
        f.write(data)

# Асинхронная функция скачивания и записи
async def download_cat(session, url, filename):
    async with session.get(url, ssl=False) as resp:
        if resp.status == 200:
            data = await resp.read()
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(None, write_file, filename, data)

async def main():
    urls = [
        "https://cataas.com/cat",
        "https://cataas.com/cat/says/hello",
        # добавь ещё при необходимости
    ]
    async with aiohttp.ClientSession() as session:
        tasks = [
            download_cat(session, url, f"cat{i}.jpg")
            for i, url in enumerate(urls)
        ]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())