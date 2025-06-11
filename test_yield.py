from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import random


class Iterator():
    ID = 0
    def __init__(self):
        self._count = 0
        Iterator.ID += 1

    def long_iterations(self):
        while self._count < 10:
            time.sleep(2)
            self._count += 1
            print(f"#{Iterator.ID} yields: {self._count}")
            yield random.randint(0, 999)  ## just return & parse outside the scrapper!

def process():
    it = Iterator()
    for item in it.long_iterations():
        return item

with ThreadPoolExecutor(max_workers=2) as executor:
    futures = [executor.submit(process), executor.submit(process), executor.submit(process)]
    for future in as_completed(futures):
        try:
            print(f"Result: {future.result()}")
        except Exception as e:
            print(f"[Runner] Error occurred: {e}")

