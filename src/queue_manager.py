"""
This module contains the queue manager for the background thread to communicate with the main thread.
"""

# Create a queue for the background thread to communicate with the main thread
import queue
import time

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
            task()
        except queue.Empty:
            pass
        time.sleep(0.1)
        print("DEBUG - Main loop running...")


def enqueue_task(task):
    """
    Enqueues a task to be executed in the main thread.
    :param task: The task to execute
    """
    _main_thread_queue.put(task)
