import random
import time
from collections import OrderedDict


# FIFO Algoritması
class FIFO:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = []

    def refer(self, page):
        if page not in self.cache:
            if len(self.cache) >= self.capacity:
                self.cache.pop(0)  # FIFO: En eski sayfa silinir
            self.cache.append(page)


# LRU Algoritması
class LRU:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = OrderedDict()  # OrderedDict kullanıyoruz

    def refer(self, page):
        if page in self.cache:
            self.cache.move_to_end(page)  # Sayfayı sonuna taşıyoruz
        elif len(self.cache) >= self.capacity:
            self.cache.popitem(last=False)  # LRU: En eski öğeyi siler
        self.cache[page] = True


# LFU Algoritması
class LFU:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}
        self.frequency = {}

    def refer(self, page):
        if page not in self.cache:
            if len(self.cache) >= self.capacity:
                # LFU: En az sıklıkla kullanılan öğeyi çıkarıyoruz
                least_frequent = min(self.frequency, key=self.frequency.get)
                self.cache.pop(least_frequent)
                self.frequency.pop(least_frequent)
            self.cache[page] = True
            self.frequency[page] = 1
        else:
            self.frequency[page] += 1


# Algoritmaların test edilmesi
def test_cache_algorithm(algorithm, pages):
    start_time = time.time()
    for page in pages:
        algorithm.refer(page)
    end_time = time.time()
    return end_time - start_time



# 1.000.000 sayfa ile test yapıyoruz
pages = [random.randint(1, 100) for _ in range(1000000)]  # 1-100 arası rastgele sayfalar
# Diğer sayfalarla rastgele bir erişim daha yapıyoruz, fakat bazı sayfalar yoğun şekilde tekrar ediyor.
for i in range(0, 1000000, 5):  # Her 5. sayfa yoğun şekilde tekrar eder
    pages[i] = random.choice(range(1, 11))  # 1-10 arası yoğun sayfalara odaklanıyoruz

capacity = 100


fifo = FIFO(capacity)
lru = LRU(capacity)
lfu = LFU(capacity)

# Test edilmesi ve sürelerin ölçülmesi
print("Testing FIFO...")
fifo_time = test_cache_algorithm(fifo, pages)
print("Testing LRU...")
lru_time = test_cache_algorithm(lru, pages)
print("Testing LFU...")
lfu_time = test_cache_algorithm(lfu, pages)

# Sonuçların yazdırılması
print(f"FIFO Time: {fifo_time:.5f} seconds")
print(f"LRU Time: {lru_time:.5f} seconds")
print(f"LFU Time: {lfu_time:.5f} seconds")