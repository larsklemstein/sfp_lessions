#!/usr/bin/env python3

import sys
import logging

import threading as t


# I hate this...
value = 0


def main():
    logging.basicConfig(level=logging.DEBUG)

    iterations = 1000000
    logging.debug(f'will execute {iterations} iterations in each thread')

    lock = t.Lock()

    adder = t.Thread(target=add, args=(iterations, lock))
    substractor = t.Thread(target=substract, args=(iterations, lock))

    logging.debug('start adder thread')
    adder.start()

    logging.debug('start substractor thread')
    substractor.start()

    logging.debug('wait for adder thread...')
    adder.join()

    logging.debug('wait for substractor thread...')
    substractor.join()

    logging.info(f'resulting value: {value}')

    sys.exit(0)


def add(n: int, lock: t.Lock):
    global value

    with lock:
        for i in range(n):
            value += 1


def substract(n: int, lock: t.Lock):
    global value

    with lock:
        for i in range(n):
            value -= 1


if __name__ == '__main__':
    main()
