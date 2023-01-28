#!/usr/bin/env python3

import threading
import time
import logging


def main():
    logging.basicConfig(level=logging.INFO) 

    tnames = ('t01', 't02', 'tn')
    tlist = []

    for tn in tnames:
        t = threading.Thread(name=tn, target=worker, args=(tn, 3))
        t.start()
        tlist.append(t)

    logging.info('Busy wait for all threads to be finished...')
    while any(t.is_alive() for t in tlist):
        time.sleep(.5)

    logging.info('done.')


def worker(wname: str, waitfor: int = 10):
    this_thread = threading.current_thread()

    logging.info(f'start thread "{wname}" (thread {this_thread}, '
                 f'os id: {this_thread.native_id})')

    time.sleep(waitfor)

    logging.info(f'end thread "{wname}"')


if __name__ == '__main__':
    main()
