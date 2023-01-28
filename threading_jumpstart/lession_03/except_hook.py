#!/usr/bin/env python3

import threading
import logging
import time


def main():
    logging.basicConfig(level=logging.INFO)

    threading.excepthook = custom_hook

    logging.info('create critical task...')
    task = threading.Thread(target=failing_task)

    logging.info('start critical task...')
    task.start()

    logging.info('join critical task...')
    task.join()

    logging.info('end main()')


def custom_hook(args):
    print('Upsi...')
    print(dir(args))
    print(dir(args.exc_traceback))


def failing_task():
    logging.info('pre critical action')
    time.sleep(0.5)
    x = 1 / 0
    logging.info('post critical action')


if __name__ == '__main__':
    main()
