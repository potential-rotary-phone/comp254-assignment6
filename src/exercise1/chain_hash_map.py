# Copyright 2013, Michael H. Goldwasser
#
# Developed for use with the book:
#
#    Data Structures and Algorithms in Python
#    Michael T. Goodrich, Roberto Tamassia, and Michael H. Goldwasser
#    John Wiley & Sons, 2013
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import time
from random import randint

from hash_map_base import HashMapBase
from unsorted_table_map import UnsortedTableMap


class ChainHashMap(HashMapBase):
    """Hash map implemented with separate chaining for collision resolution."""

    def _bucket_getitem(self, j, k):
        bucket = self._table[j]
        if bucket is None:
            raise KeyError("Key Error: " + repr(k))  # no match found
        return bucket[k]  # may raise KeyError

    def _bucket_setitem(self, j, k, v):
        if self._table[j] is None:
            self._table[j] = UnsortedTableMap()  # bucket is new to the table
        oldsize = len(self._table[j])
        self._table[j][k] = v
        if len(self._table[j]) > oldsize:  # key was new to the table
            self._n += 1  # increase overall map size

    def _bucket_delitem(self, j, k):
        bucket = self._table[j]
        if bucket is None:
            raise KeyError("Key Error: " + repr(k))  # no match found
        del bucket[k]  # may raise KeyError

    def __iter__(self):
        for bucket in self._table:
            if bucket is not None:  # a nonempty slot
                for key in bucket:
                    yield key


def test_efficiency(max_load_factors, num_items):
    results = {}
    for max_load in max_load_factors:
        hashmap = ChainHashMap(max_load=max_load)
        start_time = time.time()

        # Insert random key-value pairs
        for _ in range(num_items):
            key = randint(0, 10 * num_items)
            value = randint(0, 10 * num_items)
            hashmap[key] = value

        # Measure insertion time
        insert_time = time.time() - start_time

        # Measure retrieval time
        start_time = time.time()
        for _ in range(num_items):
            key = randint(0, 10 * num_items)
            try:
                _ = hashmap[key]
            except KeyError:
                pass
        retrieval_time = time.time() - start_time

        results[max_load] = (insert_time, retrieval_time)
    return results


def main():
    max_load_factors = [round(i * 0.1, 1) + 0.1 for i in range(10)]
    num_items = 1000
    results = test_efficiency(max_load_factors, num_items)

    print("Load Factor | Insert Time (s) | Retrieval Time (s)")
    print("-----------------------------------------------")
    for max_load, (insert_time, retrieval_time) in results.items():
        print(f"{max_load:.2f}       | {insert_time:.6f}      | {retrieval_time:.6f}")


if __name__ == "__main__":
    main()
