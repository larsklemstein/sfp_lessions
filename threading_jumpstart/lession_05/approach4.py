#!/usr/bin/env python3

"""Start 4 worker threads to fish values from a single shared queue.
   Each thread stores the sum locally and in the main function the cumulated
   value will be calculated. Use a simple None value sent to the queue to
   signal each thread that the queue is closed. Probably there are much better
   approaches than this(?)
"""


import logging
import sys
import threading
import random
import queue


def main():
    logging.basicConfig(level=logging.DEBUG)

    amount_threads = 5
    logging.debug('amount of worker threads: {amount_threads}')

    q = queue.Queue()

    for i in range(1, amount_threads+1):
        t = Counter(q, name=f't_{i:03d}')
        t.start()
        logging.debug(f'native thread id: {t.native_id}')
        logging.debug(f'main: started thread {i}')

    values = [random.randint(1, 1000) for _ in range(1000)]

    for n in values:
        q.put(n)

    for _ in range(amount_threads):
        q.put(Counter.done)

    v_total = join_threads_and_get_cumulated_result('t_')

    logging.debug(f'cumulated result: {v_total}')
    logging.debug('main: done.')
    sys.exit(0)


class Counter(threading.Thread):
    done = None

    def __init__(self, q, *args, **kwargs):
        self.__q = q
        self.__val = 0

        super().__init__(*args, **kwargs)

    def run(self):
        while True:
            input = self.__q.get()

            if input is self.done:
                logging.debug(f'thread {self. name} is done')
                break
            else:
                self.__val += input

    @property
    def value(self) -> int:
        return self.__val


def worker_threads(prefix: str = ''):
    for t in threading.enumerate():
        if t is not threading.main_thread() and t.name.startswith(prefix):
            yield t


def join_threads_and_get_cumulated_result(prefix: str = '') -> int:
    v_total = 0

    for t in worker_threads(prefix):
        logging.debug(f'thread {t.name} result: {t.value}')
        v_total += t.value
        t.join()
        logging.debug(f'joined thread {t.name}')

    return v_total


if __name__ == '__main__':
    main()
