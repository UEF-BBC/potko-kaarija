import _thread
from time import sleep_ms

lock = _thread.allocate_lock()

def other(d):
    while True:
        lock.acquire()
        n = d[0]
        l = d[1]
        q = l[n] + l[n -1]
        d[1].append(q)
        d[0] += 1
        lock.release()
        sleep_ms(100)

def main():
    d = [1, [1, 1]]
    _thread.start_new_thread(other, (d,))
    while True:
        lock.acquire()
        print(d)
        lock.release()
        sleep_ms(103)

main()