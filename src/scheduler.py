"""
Utility module for running tasks in the background at regular intervals.
"""

import threading
import time

from my_logger import general_logger

tasks = []


class BackgroundTask:
    """
    A class that represents a task that runs in the background at regular intervals.
    Required to hold a reference to the function to call and the interval at which to call it.
    """

    def __init__(self, function_to_call, interval_in_seconds):
        self.function_to_call = function_to_call
        self.interval_in_seconds = interval_in_seconds
        self.stop_event = threading.Event()  # Event to communicate to the thread that it should stop
        self.task_thread = threading.Thread(target=self.run_task)
        self.task_thread.daemon = True  # Ensures the thread will exit when the main program exits
        self.task_thread.start()

    def run_task(self):
        while not self.stop_event.is_set():
            self.function_to_call()
            time.sleep(self.interval_in_seconds)

    def stop(self):
        self.stop_event.set()
        self.task_thread.join()

    def update_interval(self, new_interval):
        self.interval_in_seconds = new_interval


def start_task(function_to_call, interval_in_seconds) -> BackgroundTask:
    """
    Starts a new task that runs the given function at the given interval.
    :return: The task object, required to modify or stop the task
    """
    task = BackgroundTask(function_to_call, interval_in_seconds)
    tasks.append(task)
    general_logger.debug(f"scheduler.start_task: Task created for function {function_to_call} with interval {interval_in_seconds} seconds. Total tasks: {len(tasks)}")
    return task


def stop_task(task):
    task.stop()
    tasks.remove(task)
