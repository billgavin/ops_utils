from collections import OrderedDict, Counter

class OrderedCounter(Counter, OrderedDict):
    '''Counter记住第一次元素出现的顺序'''

    def __repr__(self):
        return f'{self.__class__.__name__}({OrderedDict(self)})'

    def __reduce__(self):
        return self.__class__, (OrderedDict(self), )


class FIFODict(OrderedDict):
    '''FIFO（先进先出）的dict，当容量超出限制时，先删除最早添加的Key'''

    def __init__(self, capacity):
        super(FIFODict, self).__init__()
        self._capacity = capacity

    def __setitem__(self, key, value):
        containsKey = 1 if key in self else 0
        if len(self) - containsKey >= self._capacity:
            last = self.popitem(last=False)
            print(f'Remove: {last}')
        if containsKey:
            del self[key]
            print(f'set: ({key}, {value})')
        else:
            print(f'add: ({key}, {value})')
        OrderedDict.__setitem__(self, key, value)


if __name__ == '__main__':
    oc = OrderedCounter('adddddbracadabra')
    print(oc)
    ffd = FIFODict(5)
    ffd[3] = 4
    ffd[5] = 6
    print(ffd)
    ffd[3] = 2
    ffd[1] = 1
    ffd[2] = 5
    ffd[4] = 4
    ffd[0] = 0
    print(ffd)
