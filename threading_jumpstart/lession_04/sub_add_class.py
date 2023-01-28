#!/usr/bin/env python3

import sys
import logging

import threading as t


def main():
    logging.basicConfig(level=logging.DEBUG)

    value = Value()

    iterations = 10000000
    logging.debug(f'will execute {iterations} iterations in each thread')

    adder = t.Thread(target=add, args=(value, iterations))
    substractor = t.Thread(target=substract, args=(value, iterations))

    logging.debug('start adder thread')
    adder.start()

    logging.debug('start substractor thread')
    substractor.start()

    logging.debug('wait for adder thread...')
    adder.join()

    logging.debug('wait for substractor thread...')
    substractor.join()

    logging.info(f'resulting value: {value.val}')
    sys.exit(0)


class Value:
    def __init__(self, start_val=0):
        self.__val = start_val

    def __add__(self, v):
        self.__val += v
        return self

    def __sub__(self, v):
        self.__val -= v
        return self

    @property
    def val(self):
        return self.__val


def add(value, n):
    for i in range(n):
        value = value + 1
        # print('a', value.val)


def substract(value, n):
    for i in range(n):
        value = value - 1
        # print('s', value.val)


if __name__ == '__main__':
    main()
