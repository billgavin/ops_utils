import json

class SingleNode(object):
    '''单向节点'''

    def __init__(self, data, pnext=None):
        self.data = data if type(data) is not set else list(data)
        self.pnext = pnext

    def getNode(self):
        node = {'Data': self.data, 'Next': hex(id(self.pnext)) if self.pnext is not None else None, 'Self': hex(id(self))}
        return node

    def __repr__(self):
        return json.dumps(self.getNode())

    def __str__(self):
        return self.__repr__()
        


class SingleChainTable(object):

    def __init__(self, cycler=False):
        self.head = None
        self.tail = None
        self.length = 0
        self.cycler = cycler

    def isEmpty(self):
        '''判断链表是否为空'''
        return self.head is None

    def _travelNode(self):
        '''遍历链表,返回节点类型'''
        if self.isEmpty():
            return []
        curr = self.head
        result = [{'Cycler': self.cycler, 'Length': self.length, 'Head': hex(id(self.head)), \
                'Tail': hex(id(self.tail))}, curr.getNode()]
        while (curr.pnext is not None) and (curr.pnext != self.head):
            curr = curr.pnext
            result.append(curr.getNode())
        return result

    def __repr__(self):
        return json.dumps(self._travelNode(), indent=4)

    def __len__(self):

    def travel(self):
        '''遍历链表，返回数据'''
        return [i['Data'] for i in self._travelNode()[1:]]

    def add(self, data):
        '''头部添加节点'''
        node = SingleNode(data)
        #长度加1
        self.length += 1
        if self.isEmpty():
            #头尾都指向新节点
            self.head = node
            self.tail = node
            if self.cycler:
                #循环链表尾节点next指向头节点
                node.pnext = self.head
        else:
            #新节点next指向原来头节点
            node.pnext = self.head
            #头指针指向新节点
            self.head = node
            if self.cycler:
                #循环链表修改原尾节点next指向新的头节点
                self.tail.pnext = node

    def append(self, data):
        '''尾部添加节点'''
        node = SingleNode(data)
        #长度加1
        self.length += 1
        if self.isEmpty():
            #头尾都指向新节点
            self.head = node
            self.tail = node
            if self.cycler:
                #循环链表尾节点next指向头节点
                node.pnext = self.head
        else:
            #修改原尾节点next指向新节点
            self.tail.pnext = node
            #尾指针指向新节点
            self.tail = node
            if self.cycler:
                #循环链表尾节点next指向头节点
                node.pnext = self.head

    def insert(self, pos, data):
        '''在指定位置添加节点'''
        if pos <= 0:
            #头部添加
            self.add(data)
        elif pos >= self.length:
            #尾部添加
            self.append(data)
        else:
            node = SingleNode(data)
            self.length += 1
            curr = self.head
            for i in range(pos - 1):
                curr = curr.pnext
            node.pnext = curr.pnext
            curr.pnext = node

    @classmethod
    def create(cls, *data, cycler=False):
        sct = cls(cycler=cycler)
        for d in data:
            sct.append(d)
        return sct

    def delete(self, pos):
        '''删除节点'''
        if self.isEmpty() or pos < 0 or pos >= self.length:
            print('This chain table is empty or out of index.')
            return
        if pos == 0:
            self.head = self.head.pnext
            self.length -= 1
            if self.cycler:
                self.tail.pnext = self.head
            return

        curr = self.head
        prev = self.head
        for i in range(pos):
            prev = curr
            curr = curr.pnext
        prev.pnext = curr.pnext
        if pos == (self.length - 1):
            self.tail = prev
        self.length -= 1

    def update(self, pos, data):
        if self.isEmpty() or pos < 0 or pos >= self.length:
            print('This chain table is empty or out of index.')
        i = 0
        curr = self.head
        while curr.pnext and i < pos:
            curr = curr.pnext
            i += 1
        if i == pos:
            curr.data = data

    def get(self, pos):
        if self.isEmpty() or pos < 0 or pos >= self.length:
            print('This chain table is empty or out of index.')
            return None
        i = 0
        curr = self.head
        while curr.pnext and i < pos:
            curr = curr.pnext
            i += 1
        return curr.data

    def search(self, data):
        if self.isEmpty():
            print('This chain table is empty.')
            return []
        result = []
        for i, d in enumerate(self.travel()):
            if d == data:
                result.append(i)
        return result

    def clear(self):
        '''清空链表'''
        self.head = None
        self.tail = None
        self.length = 0



class DoubleNode(object):
    '''双向节点'''
    
    def __init__(self, data, prev=None, pnext=None):
        self.prev = prev
        self.data = data if type(data) is not set else list(data)
        self.pnext = pnext

    def getNode(self):
        node = {'Data': self.data, 'Prev': hex(id(self.prev)) if self.prev is not None else None, 'Next': hex(id(self.pnext)) if self.pnext is not None else None, 'Self': hex(id(self))}
        return node

    def __repr__(self):
        return json.dumps(self.getNode())

    def __str__(self):
        return self.__repr__()


class DoubleChainTable(object):

    def __init__(self, cycler=False):
        self.head = None
        self.tail = None
        self.length = 0
        self.cycler = cycler

if __name__ == '__main__':
    sctc = SingleChainTable.create({1: 'a', 'rt': 3}, cycler=True)
    print(sctc)
    sctc.append({'a':3, 3: 'a'})
    print(sctc)
