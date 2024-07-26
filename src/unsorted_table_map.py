from collections.abc import MutableMapping


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


class UnsortedTableMap(MapBase):
    def _find_index(self, k, low, high):
        if high < low:
            return high + 1
        else:
            mid = (low + high) // 2
            if k == self._table[mid]._key:
                return mid
            elif k < self._table[mid]._key:
                return self._find_index(k, low, mid - 1)
            else:
                return self._find_index(k, mid + 1, high)

    def __init__(self):
        self._table = []

    def __getitem__(self, k):
        for item in self._table:
            if k == item._key:
                return item._value
        raise KeyError("Key Error: " + repr(k))

    def __setitem__(self, k, v):
        for item in self._table:
            if k == item._key:
                item._value = v
                return
        self._table.append(self._Item(k, v))

    def __delitem__(self, k):
        for j in range(len(self._table)):
            if k == self._table[j]._key:
                self._table.pop(j)
                return
        raise KeyError("Key Error: " + repr(k))

    def __len__(self):
        return len(self._table)

    def __iter__(self):
        for item in self._table:
            yield item._key

    def containKey(self, k):
        index = self._find_index(k, 0, len(self._table) - 1)
        return index < len(self._table) and self._table[index]._key == k


# Main method to test the solution
def main():
    m = UnsortedTableMap()
    m["a"] = 1
    m["b"] = 2
    m["c"] = 3

    print("Contain 'a':", m.containKey("a"))  # Expected: True
    print("Contain 'b':", m.containKey("b"))  # Expected: True
    print("Contain 'c':", m.containKey("c"))  # Expected: True
    print("Contain 'd':", m.containKey("d"))  # Expected: False

    del m["b"]
    print("Contain 'b' after deletion:", m.containKey("b"))  # Expected: False


if __name__ == "__main__":
    main()
