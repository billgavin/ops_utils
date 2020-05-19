import fire
import time
import random
import queue
import threadpool

def isOrdered(*a):
    return all([a[i] <= a[i + 1] for i in range(len(a) - 1)]) or all([a[i] >= a[i + 1] for i in range(len(a) - 1)])

def bogoSort(*a):
    la = list(a)
    if isOrdered(*la):
        print('Ordered.')
        pass
    else:
        count = 0
        start = time.time()
        while not isOrdered(*la):
            random.shuffle(la)
            count += 1
        end = time.time()
        print(f'monkey, {count} times, {int(end-start)}s')
    return la


def sleepPut(num):
    time.sleep(num / 100)
    queue.put(num)

def sleepSort(*a):
    start = time.time() * 1000
    global queue
    queue = queue.Queue()
    mina = min(a)
    lvars = []
    for i in a:
        lvars.append(i - mina)
    pool = threadpool.ThreadPool(len(lvars))
    requests = threadpool.makeRequests(sleepPut, lvars)
    [pool.putRequest(req) for req in requests]
    pool.wait()
    res = []
    while not queue.empty():
        res.append(queue.get() + mina)
    print(f'running {time.time() * 1000 - start}ms')
    return res

def gnomeSort(*a):
    la = list(a)
    index = 1
    while index < len(la):
        if index > 0 and la[index] < la[index - 1]:
            la[index], la[index - 1] = la[index - 1], la[index]
            index -= 1
        else:
            index += 1
    return la

if __name__ == '__main__':
    fire.Fire()
