#!/usr/bin/env python3

import logging
import random
import threading
import time

def main():
    run_tasks(1000, 100)

def task_runner(semaphore: threading.Semaphore, tname: str) -> None:
    logger = logging.getLogger()

    created_threads = [t for t in threading.enumerate() if t.name.startswith('t_')]
    amount_created_threads = len(created_threads)
    logger.info(f'created threads: {amount_created_threads}')

    with semaphore:
        logger.info(f'start task {tname}')

        active_threads = [t for t in threading.enumerate() if t.is_alive()]
        amount_active_threads = len(active_threads)
        logger.info(f'active threads: {amount_active_threads}')

        sleep_time = random.random()
        logger.info(f'task {tname} will sleep for {sleep_time:.3f} seconds...')
        time.sleep(sleep_time)

    logger.info(f'end task {tname}')

def run_tasks(amount_tasks, parallel_tasks: int) -> None:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(threadName)s - %(message)s'
    )

    logger = logging.getLogger()

    semaphore = threading.Semaphore(parallel_tasks)

    tasks = [threading.Thread(name=f't_{i:03d}', target=task_runner, args=(semaphore, i))
             for i in range(1, amount_tasks+1)]
    logger.info(f'created {amount_tasks} tasks')

    for task in tasks:
        task.start()

    logger.info(f'going to join {amount_tasks} tasks...')
    for task in tasks:
        task.join()

    logger.info('done.')


    
if __name__ == '__main__':
    main()
