#!/usr/bin/env python3

import sys
import logging

import threading as t


# I hate this...
value = 0


def main():
    logging.basicConfig(level=logging.DEBUG)

    iterations = 100 * 1000
    logging.debug(f'will execute {iterations} iterations in each thread')

    semaphore = t.Semaphore(1)

    adder = t.Thread(target=add, args=(iterations, semaphore))
    substractor = t.Thread(target=substract, args=(iterations, semaphore))

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


def add(n: int, semaphore: t.Semaphore):
    global value

    for _ in range(n):
        with semaphore:
            value += 1


def substract(n: int, semaphore: t.Semaphore):
    global value

    for _ in range(n):
        with semaphore:
            value -= 1


if __name__ == '__main__':
    main()
