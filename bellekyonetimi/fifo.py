import time
from collections import deque, OrderedDict, Counter

# FIFO Algoritması
class FIFOCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = deque()
        self.cache_set = set()

    def access(self, page: int):
        if page in self.cache_set:
            return "Vuruş"

        if len(self.cache) >= self.capacity:
            oldest_page = self.cache.popleft()
            self.cache_set.remove(oldest_page)

        self.cache.append(page)
        self.cache_set.add(page)
        return "Kaçırma"

# LRU Algoritması
class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = OrderedDict()

    def access(self, page: int):
        if page in self.cache:
            self.cache.move_to_end(page)  # En son kullanılanı sona al
            return "Vuruş"

        if len(self.cache) >= self.capacity:
            self.cache.popitem(last=False)  # En eskiyi sil

        self.cache[page] = True
        return "Kaçırma"

# LFU Algoritması
class LFUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}
        self.frequency = Counter()

    def access(self, page: int):
        if page in self.cache:
            self.frequency[page] += 1  # Kullanım sayısını artır
            return "Vuruş"

        if len(self.cache) >= self.capacity:
            least_frequent_page = min(self.frequency, key=self.frequency.get)  # En az kullanılanı bul
            del self.cache[least_frequent_page]  # Sil
            del self.frequency[least_frequent_page]

        self.cache[page] = True
        self.frequency[page] = 1
        return "Kaçırma"

# Test Senaryosu - FIFO’nun En Hızlı Olduğu Durum
access_sequence = list(range(1, 1000000))  # 1'den 1000000'e kadar artan sayfa dizisi
cache_size = 50  # Önbellek kapasitesi 50 olsun

# Algoritmaları Test Eden Fonksiyon
def test_cache(cache_class, access_sequence):
    cache = cache_class(cache_size)
    hits, misses = 0, 0
    start_time = time.time()

    for page in access_sequence:
        result = cache.access(page)
        if result == "Vuruş":
            hits += 1
        else:
            misses += 1

    end_time = time.time()
    return hits, misses, end_time - start_time

# Algoritmaları Çalıştırma
fifo_hits, fifo_misses, fifo_time = test_cache(FIFOCache, access_sequence)
lru_hits, lru_misses, lru_time = test_cache(LRUCache, access_sequence)
lfu_hits, lfu_misses, lfu_time = test_cache(LFUCache, access_sequence)

# Sonuçları Yazdırma
print(f"FIFO: Hits = {fifo_hits}, Misses = {fifo_misses}, Time = {fifo_time:.6f} seconds")
print(f"LRU : Hits = {lru_hits}, Misses = {lru_misses}, Time = {lru_time:.6f} seconds")
print(f"LFU : Hits = {lfu_hits}, Misses = {lfu_misses}, Time = {lfu_time:.6f} seconds")