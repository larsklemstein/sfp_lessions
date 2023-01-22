#!/usr/bin/env python3

import sys
import logging

import threading as t


# I hate this...
value = 0


def main():
    logging.basicConfig(level=logging.DEBUG)

    iterations = 1000000
    logging.debug('will execute %d iterations in each thread' % iterations)

    adder = t.Thread(target=add, args=(iterations,))
    substractor = t.Thread(target=substract, args=(iterations,))

    logging.debug('start adder thread')
    adder.start()

    logging.debug('start substractor thread')
    substractor.start()

    logging.debug('wait for adder thread...')
    adder.join()

    logging.debug('wait for substractor thread...')
    substractor.join()

    logging.info('resulting value: ' + str(value))

    if value == 0:
        logging.info('BUT WHY?!?')

    sys.exit(0)


def add(n: int):
    global value

    for i in range(n):
        value += 1


def substract(n: int):
    global value

    for i in range(n):
        value -= 1


if __name__ == '__main__':
    main()
