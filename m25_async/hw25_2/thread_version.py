# thread_version.py
import requests
import threading
import time

def download_cat(url, filename):
    response = requests.get(url, verify=False)  # verify=False отключает SSL проверку
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)

def main(num_images=10):
    url = "https://cataas.com/cat"
    threads = []

    for i in range(num_images):
        t = threading.Thread(target=download_cat, args=(url, f"thread_cat_{i}.jpg"))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

if __name__ == "__main__":
    start = time.time()
    main(100)
    end = time.time()
    print(f"Thread download time: {end - start:.2f} sec")