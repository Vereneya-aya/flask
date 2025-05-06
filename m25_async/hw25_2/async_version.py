# async_version.py
import asyncio
import aiohttp
import time

def save_image(path, data):
    with open(path, 'wb') as f:
        f.write(data)

async def download_cat(session, url, filename):
    async with session.get(url, ssl=False) as resp:
        if resp.status == 200:
            data = await resp.read()
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(None, save_image, filename, data)

async def main(num_images=10):
    url = "https://cataas.com/cat"
    async with aiohttp.ClientSession() as session:
        tasks = [
            download_cat(session, url, f"async_cat_{i}.jpg")
            for i in range(num_images)
        ]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    start = time.time()
    asyncio.run(main(100))
    end = time.time()
    print(f"Async download time: {end - start:.2f} sec")