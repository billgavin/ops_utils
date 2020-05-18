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
    print(f'Thread sleep {num}ms')
    time.sleep(num / 1000)
    queue.put(num)

def sleepSort(*a):
    start = time.time() * 1000
    global queue
    queue = queue.Queue()
    lvars = list(a)
    pool = threadpool.ThreadPool(len(lvars))
    requests = threadpool.makeRequests(sleepPut, lvars)
    [pool.putRequest(req) for req in requests]
    pool.wait()
    res = []
    while not queue.empty():
        res.append(queue.get())
    print(f'running {time.time() * 1000 - start}ms')
    return res


if __name__ == '__main__':
    fire.Fire()
