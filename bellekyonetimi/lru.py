import time
from collections import deque, Counter


# FIFO Cache (First-In-First-Out)
class FIFO:
    def __init__(self, cache_size):
        self.cache_size = cache_size
        self.cache = deque()

    def access(self, page):
        if page not in self.cache:
            if len(self.cache) == self.cache_size:
                self.cache.popleft()  # Remove the oldest page
            self.cache.append(page)


# LRU Cache (Least Recently Used) - Optimized with Doubly Linked List + HashMap
class Node:
    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LRUCache:
    def __init__(self, cache_size):
        self.cache_size = cache_size
        self.cache = {}  # HashMap to store key -> Node
        self.head = Node()  # Dummy head of the doubly linked list
        self.tail = Node()  # Dummy tail of the doubly linked list
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node):
        """Remove node from the linked list."""
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node

    def _insert_at_end(self, node):
        """Insert node at the end (most recently used position)."""
        prev_node = self.tail.prev
        prev_node.next = node
        node.prev = prev_node
        node.next = self.tail
        self.tail.prev = node

    def access(self, page):
        if page in self.cache:
            # Move the accessed node to the end (most recently used)
            node = self.cache[page]
            self._remove(node)
            self._insert_at_end(node)
        else:
            # If not found, create a new node
            if len(self.cache) >= self.cache_size:
                # Remove the least recently used node
                lru_node = self.head.next
                self._remove(lru_node)
                del self.cache[lru_node.key]

            new_node = Node(page)
            self.cache[page] = new_node
            self._insert_at_end(new_node)


# LFU Cache (Least Frequently Used)
class LFU:
    def __init__(self, cache_size):
        self.cache_size = cache_size
        self.cache = {}
        self.frequency = Counter()

    def access(self, page):
        if len(self.cache) >= self.cache_size and page not in self.cache:
            least_frequent_page = min(self.frequency, key=self.frequency.get)
            del self.cache[least_frequent_page]
            del self.frequency[least_frequent_page]
        self.cache[page] = True
        self.frequency[page] += 1


# Function to test each cache algorithm and return the time taken
def test_cache(cache_algo, cache_size, pages):
    start_time = time.time()
    for page in pages:
        cache_algo.access(page)
    return time.time() - start_time


# Sample test scenario with more pages
# Simulating 10,000 page accesses for testing
pages = [i % 100 for i in range(1000000)]  # Repeating numbers to simulate a larger dataset
cache_size = 100  # Test with larger cache size

print("Testing with larger dataset of 10,000 page accesses and cache size of 100:")

# Testing FIFO
fifo_cache = FIFO(cache_size)
fifo_time = test_cache(fifo_cache, cache_size, pages)
print(f"FIFO Time: {fifo_time:.6f} seconds")

# Testing LRU (Optimized with Doubly Linked List + HashMap)
lru_cache = LRUCache(cache_size)
lru_time = test_cache(lru_cache, cache_size, pages)
print(f"LRU Time: {lru_time:.6f} seconds")

# Testing LFU
lfu_cache = LFU(cache_size)
lfu_time = test_cache(lfu_cache, cache_size, pages)
print(f"LFU Time: {lfu_time:.6f} seconds")

