#!/usr/bin/env python3

import logging
import threading
import time


def main():
    logging.basicConfig(level=logging.INFO)

    amount_tasks = 5
    wait_time = 1.0

    time_serially = run_tasks_serially(amount_tasks, wait_time)
    time_parallel = run_tasks_parallel(amount_tasks, wait_time)

    logging.info(
        f'exec time of {amount_tasks} tasks serially: {time_serially:.3f}')
    logging.info(
        f'exec time of {amount_tasks} tasks parallel: {time_parallel:.3f}')

    ratio = time_serially / time_parallel
    logging.info(f'ratio (time serially / time parallel) is {ratio:.3f}')


def run_tasks_serially(amount_tasks, wait_time: float) -> int:
    time_start = time.time()

    for n in range(amount_tasks):
        the_task(f'serial_{n}', wait_time)

    time_end = time.time()

    return time_end - time_start


def run_tasks_parallel(amount_tasks, wait_time: float) -> int:
    time_start = time.time()

    tasks = []

    for n in range(amount_tasks):
        task = threading.Thread(
            name=n, target=the_task, args=(f'parallel_{n}', wait_time,))
        task.start()
        tasks.append(task)

    for task in tasks:
        task.join()

    time_end = time.time()

    return time_end - time_start


def the_task(tname: str, wait_time: int) -> None:
    logging.info(f'start task {tname}')
    time.sleep(wait_time)
    logging.info(f'end task {tname}')


if __name__ == '__main__':
    main()
