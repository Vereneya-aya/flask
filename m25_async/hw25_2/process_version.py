# process_version.py
import requests
import multiprocessing
import time

def download_cat(url, filename):
    response = requests.get(url, verify=False)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)

def main(num_images=10):
    url = "https://cataas.com/cat"
    processes = []

    for i in range(num_images):
        p = multiprocessing.Process(target=download_cat, args=(url, f"process_cat_{i}.jpg"))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

if __name__ == "__main__":
    start = time.time()
    main(100)
    end = time.time()
    print(f"Process download time: {end - start:.2f} sec")