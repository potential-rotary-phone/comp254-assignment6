from random import randrange
from collections.abc import MutableMapping
import time


class MapBase(MutableMapping):
    class _Item:
        __slots__ = "_key", "_value"

        def __init__(self, k, v):
            self._key = k
            self._value = v

        def __eq__(self, other):
            return self._key == other._key

        def __ne__(self, other):
            return not (self == other)

        def __lt__(self, other):
            return self._key < other._key


class HashMapBase(MapBase):
    def __init__(self, cap=11, p=109345121, max_load=0.5):
        self._table = cap * [None]
        self._n = 0
        self._prime = p
        self._scale = 1 + randrange(p - 1)
        self._shift = randrange(p)
        self._max_load = max_load

    def _hash_function(self, k):
        return (hash(k) * self._scale + self._shift) % self._prime % len(self._table)

    def __len__(self):
        return self._n

    def __getitem__(self, k):
        j = self._hash_function(k)
        return self._bucket_getitem(j, k)

    def __setitem__(self, k, v):
        j = self._hash_function(k)
        self._bucket_setitem(j, k, v)
        if self._n > len(self._table) * self._max_load:
            self._resize(2 * len(self._table) - 1)

    def __delitem__(self, k):
        j = self._hash_function(k)
        self._bucket_delitem(j, k)
        self._n -= 1

    def _resize(self, c):
        old = list(self.items())
        self._table = c * [None]
        self._n = 0
        for k, v in old:
            self[k] = v


class ProbeHashMap(HashMapBase):
    _AVAIL = object()

    def _is_available(self, j):
        return self._table[j] is None or self._table[j] is ProbeHashMap._AVAIL

    def _find_slot(self, j, k):
        firstAvail = None
        while True:
            if self._is_available(j):
                if firstAvail is None:
                    firstAvail = j
                if self._table[j] is None:
                    return (False, firstAvail)
            elif k == self._table[j]._key:
                return (True, j)
            j = (j + 1) % len(self._table)

    def _bucket_getitem(self, j, k):
        found, s = self._find_slot(j, k)
        if not found:
            raise KeyError("Key Error: " + repr(k))
        return self._table[s]._value

    def _bucket_setitem(self, j, k, v):
        found, s = self._find_slot(j, k)
        if not found:
            self._table[s] = self._Item(k, v)
            self._n += 1
        else:
            self._table[s]._value = v

    def _bucket_delitem(self, j, k):
        found, s = self._find_slot(j, k)
        if not found:
            raise KeyError("Key Error: " + repr(k))
        self._table[s] = ProbeHashMap._AVAIL

    def __iter__(self):
        for j in range(len(self._table)):
            if not self._is_available(j):
                yield self._table[j]._key


# Testing the implementation


def test_efficiency(max_load_factors, num_items):
    results = {}
    for max_load in max_load_factors:
        hashmap = ProbeHashMap(max_load=max_load)
        start_time = time.time()

        # Insert random key-value pairs
        for _ in range(num_items):
            key = randrange(10 * num_items)
            value = randrange(10 * num_items)
            hashmap[key] = value

        # Measure insertion time
        insert_time = time.time() - start_time

        # Measure retrieval time
        start_time = time.time()
        for _ in range(num_items):
            key = randrange(10 * num_items)
            try:
                _ = hashmap[key]
            except KeyError:
                pass
        retrieval_time = time.time() - start_time

        results[max_load] = (insert_time, retrieval_time)
    return results


def main():
    max_load_factors = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    num_items = 1000
    results = test_efficiency(max_load_factors, num_items)

    print("Load Factor | Insert Time (s) | Retrieval Time (s)")
    print("-----------------------------------------------")
    for max_load, (insert_time, retrieval_time) in results.items():
        print(f"{max_load:.2f}       | {insert_time:.6f}      | {retrieval_time:.6f}")


if __name__ == "__main__":
    main()
