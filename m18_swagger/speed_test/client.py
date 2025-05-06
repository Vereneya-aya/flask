# client.py
import requests
import time
import threading
from concurrent.futures import ThreadPoolExecutor

class APITester:
    def __init__(self, url, num_requests=10, use_session=False, use_threads=False):
        self.url = url
        self.num_requests = num_requests
        self.use_session = use_session
        self.use_threads = use_threads

    def make_request(self, session=None):
        if session:
            response = session.get(self.url)
        else:
            response = requests.get(self.url)
        return response

    def run(self):
        start = time.time()
        if self.use_threads:
            with ThreadPoolExecutor() as executor:
                if self.use_session:
                    with requests.Session() as session:
                        executor.map(lambda _: self.make_request(session), range(self.num_requests))
                else:
                    executor.map(lambda _: self.make_request(), range(self.num_requests))
        else:
            if self.use_session:
                with requests.Session() as session:
                    for _ in range(self.num_requests):
                        self.make_request(session)
            else:
                for _ in range(self.num_requests):
                    self.make_request()
        end = time.time()
        return end - start

if __name__ == "__main__":
    url = "http://localhost:5000/ping"
    tests = [
        {"num_requests": 1000, "use_session": False, "use_threads": False},
        {"num_requests": 1000, "use_session": True, "use_threads": False},
        {"num_requests": 1000, "use_session": False, "use_threads": True},
        {"num_requests": 1000, "use_session": True, "use_threads": True},
        # Повтори для 100, 1000
    ]

    for test in tests:
        tester = APITester(url, **test)
        t = tester.run()
        print(f"Requests: {test['num_requests']}, Session: {test['use_session']}, Threads: {test['use_threads']}, Time: {t:.3f} сек")