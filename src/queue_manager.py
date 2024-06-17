"""
This module contains the queue manager for the background thread to communicate with the main thread.
"""

# Create a queue for the background thread to communicate with the main thread
import queue
import time

from my_logger import general_logger

_main_thread_queue = queue.Queue()


def main_loop():
    """
    The main loop of the program.
    This function is called from the main thread and runs in a loop, checking for tasks to execute.
    """
    print("Main loop starting...")
    while True:
        try:
            task = _main_thread_queue.get_nowait()
            general_logger.debug(f"Dequeued task: {task.__name__} ({task})")
            task()
        except queue.Empty:
            pass
        time.sleep(0.1)


def enqueue_task(task):
    """
    Enqueues a task to be executed in the main thread.
    :param task: The task to execute
    """
    general_logger.debug(f"Enqueuing task: {task.__name__} ({task})")
    _main_thread_queue.put(task)
