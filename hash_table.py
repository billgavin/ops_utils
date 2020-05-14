from collections import namedtuple
import prettytable as pt
import hashlib
import fire

class HashTable(object):

    def __init__(self, size=10):
        self.size = size
        self.table = [[] for i in range(size)]
        self.columns = {i: 0 for i in range(size)}

    def hash(self, key):
        #assert type(key) not in [int, float, str, tuple], 'Key must be immutable type.'
        hm = hashlib.md5()
        hm.update(str(key).encode(encoding='UTF-8'))
        hexkey = hm.hexdigest()
        return int(hexkey, 16) % self.size

    def insert(self, key, value):
        Node = namedtuple('Node', 'Key, Value')
        index = self.hash(key)
        items = self.table[index]
        column = self.columns[index]
        if items:
            for item in items:
                if key == item[0]:
                    items.remove(item)
                    column -= 1
                    break
        items.append(Node(key, value))
        column += 1
        self.table[index] = items
        self.columns[index] = column
    
    @classmethod
    def create(cls, size=10, **items):
        ht = cls(size)
        for k, v in items.items():
            ht.insert(k, v)
        return ht

    def get(self, key):
        index = self.hash(key)
        if self.table[index]:
            for item in self.table[index]:
                if key == item[0]:
                    return item[1]
                else:
                    return None
        else:
            return None

    def __setitem__(self, key, value):
        return self.insert(key, value)

    def __getitem__(self, key):
        return self.get(key)

    def __len__(self):
        return self.size

    def __repr__(self):
        tb = pt.PrettyTable()
        max_col = max(self.columns.values())
        tb.field_names = [i for i in range(max_col)]
        for row in self.table:
            tb.add_row(row)
        return tb

if __name__ == '__main__':
    #fire.Fire()
    ht = HashTable.create(size=5,a=1, b=2, c=3, d=4, e=5)
    #ht = HashTable()
    ht.insert(1, 1)
    print(ht)
