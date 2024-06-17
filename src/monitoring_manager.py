"""
This module is responsible for managing the monitors. It provides methods to add, remove, and update monitors.
It also provides methods to save and load the monitors to and from a file.
"""

import json
import os
from typing import List
from blinker import signal

from monitor_object import MonitorObject
from my_logger import general_logger
from scheduler import BackgroundTask, start_task


def get_monitor_list_json() -> str:
    return convert_monitors_list_to_json(_monitors)


def save_monitors_to_file() -> None:
    with open("monitors_data.json", "w") as file:
        json_data = convert_monitors_list_to_json(_monitors)
        file.write(json_data)
        general_logger.debug(f"Monitors saved to monitors_data.json")


def get_monitor_by_title(title: str) -> MonitorObject | None:
    # HACK - We're using the monitor's title as its "unique" id in the prototype, terrible idea but eh
    for monitor in _monitors:
        if monitor.title == title:
            return monitor
    return None


def update_monitors_list_from_loca_json_file() -> None:
    global _monitors
    _monitors = read_monitors_list_from_file()


def read_monitors_json_from_file() -> str:
    # Create an empty monitors_data.json file if it doesn't exist
    if not os.path.exists("monitors_data.json"):
        with open("monitors_data.json", "w") as file:
            file.write("[]")
            general_logger.warning('Monitor config "monitors_data.json" not found. Created an empty file.')
            return ""
    else:
        try:
            with open("monitors_data.json", "r") as file:
                file_content = file.read()
                general_logger.debug(f"read_monitors_json_from_file: {file_content}")
                return file_content
        except FileNotFoundError:
            general_logger.error("monitors_data.json could not be found.")
            return ""
        except Exception as e:
            general_logger.error(f"An error occurred while reading monitors_data.json: {e}")
            return ""


def read_monitors_list_from_file() -> List[MonitorObject]:
    return convert_monitors_json_to_list(read_monitors_json_from_file())


def append_monitor(monitor: MonitorObject) -> None:
    _monitors.append(monitor)
    save_monitors_to_file()


def create_and_append_monitor(title: str, url: str, test_interval_in_seconds: int) -> MonitorObject:
    new_monitor = MonitorObject(title, url, test_interval_in_seconds)
    append_monitor(new_monitor)
    return new_monitor


def remove_monitor(monitor: MonitorObject) -> None:
    _monitors.remove(monitor)
    save_monitors_to_file()


def update_monitors_from_json(monitor_data_json: str) -> None:
    """
    Rebuilds the monitors list with the data from the JSON string
    """
    global _monitors
    _monitors = convert_monitors_json_to_list(monitor_data_json)
    general_logger.debug(f"update_monitors_from_json: {_monitors}")
    save_monitors_to_file()


def convert_monitors_json_to_list(monitor_data_json: str) -> List[MonitorObject]:
    if monitor_data_json == "":
        general_logger.info("Monitor config data is empty.")
        return []
    else:
        try:
            monitor_dicts = json.loads(monitor_data_json)
        except json.JSONDecodeError:
            general_logger.error("Error parsing monitor config JSON. Returning an empty list.")
            monitor_dicts = []

    # Convert test_interval_in_seconds to integer
    for monitor in monitor_dicts:
        monitor["test_interval_in_seconds"] = int(monitor["test_interval_in_seconds"])

    monitors_list = [MonitorObject(**monitor_dict) for monitor_dict in monitor_dicts]

    general_logger.debug(f"convert_monitors_json_to_list: {monitors_list} monitors parsed from JSON")

    return monitors_list


def convert_monitors_list_to_json(monitor_data_list: List[MonitorObject]) -> str:
    monitor_dicts = [monitor.__dict__ for monitor in monitor_data_list]
    return json.dumps(monitor_dicts)


_monitors: List[MonitorObject] = read_monitors_list_from_file()  # The list of monitors
_monitoring_task: BackgroundTask | None = None  # The task that will run in the background to monitor the monitors
tests_executed_signal = signal("tests-executed")  # Signal to be emitted when tests are executed, used to signal changes to the GUI


def start_monitoring() -> None:
    """
    Starts the monitoring task that will go through all monitors to execute their tests if they are due
    """
    general_logger.info("Monitoring started.")
    global _monitoring_task
    if _monitoring_task is not None:
        general_logger.debug("Another monitoring task exists, it will be stopped before starting a new one.")
        _monitoring_task.stop()
    _monitoring_task = start_task(execute_all_due_tests, 1)


def stop_monitoring() -> None:
    general_logger.info("Monitoring stopped")
    global _monitoring_task
    _monitoring_task.stop()


def execute_all_due_tests() -> None:
    """
    The function passed to the BackgroundTask that will execute all tests that are due
    """
    any_test_executed = False
    for monitor in _monitors:
        test_ran = monitor.execute_test_if_due()
        if test_ran:
            any_test_executed = True

    if any_test_executed:
        save_monitors_to_file()
        tests_executed_signal.send()
    else:
        # print("No tests were due")
        pass
