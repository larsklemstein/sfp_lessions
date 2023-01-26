#!/usr/bin/env python3

"""Share data between threads using a shared, thread save(?) object

Used concepts:
    - threading.enumerate (instead of maintaining our own thread list)
    - join with timeout
    - is_alive to check for occured timeout (savely?)
"""


import logging
import threading
import time
import sys


def main():
    amount_threads = 5
    timeout_join = 2

    logging.basicConfig(level=logging.DEBUG)

    v = Value()
    logging.debug('created value object')

    for i in range(amount_threads):
        t_name = f't_{i:03d}'
        t = threading.Thread(target=increment, name=t_name, args=(v, 3,))
        t.start()
        logging.debug(f'started thread {t_name}')

    t_main = threading.main_thread()
    for t in threading.enumerate():
        if t is not t_main:
            t_name = t.name
            logging.debug(f'joining thread {t_name}...')
            t.join(timeout=timeout_join)

            if t.is_alive():
                logging.warning(
                    f'...thread {t_name} is still alive after join timeout!')
            else:
                logging.debug('...OK')
        
    logging.debug(f'resulting value is {v.value}')
    sys.exit(0)


class Value:
    def __init__(self, v=0):
        self.__v = v
        self.__lock = threading.Lock()

    @property
    def value(self):
        return self.__v

    def change_value(self, v_new):
        assert v_new != self.__v
        with self.__lock:
            self.__v = v_new


def increment(v, n_times, by=1, sleep=0.2):
    for _ in range(n_times):
       v.change_value(v.value + by)
       time.sleep(sleep)
        

if __name__ == '__main__':
    main()
