#!/usr/bin/env python3

"""Share data between threads using a global variable
"""


import logging
import threading
import time
import sys


VALUE = 0


def main():
    amount_threads = 5

    logging.basicConfig(level=logging.DEBUG)

    lock = threading.Lock()

    for i in range(amount_threads):
        t_name = f't_{i:03d}'
        t = threading.Thread(target=increment, name=t_name, args=(lock, 3,))
        t.start()
        logging.debug(f'started thread {t_name}')

    t_main = threading.main_thread()
    for t in threading.enumerate():
        if t is not t_main:
            t_name = t.name
            logging.debug(f'joining thread {t_name}...')
            t.join()
            logging.debug('...OK')
        
    logging.debug(f'resulting value is {VALUE}')
    sys.exit(0)



def increment(lock, n_times, by=1, sleep=0.2):
    global VALUE

    for _ in range(n_times):
        with lock:
            VALUE += by
            time.sleep(sleep)
        

if __name__ == '__main__':
    main()
