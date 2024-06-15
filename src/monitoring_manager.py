"""
This module is responsible for managing the monitors. It provides methods to add, remove, and update monitors.
It also provides methods to save and load the monitors to and from a file.
"""

import json
from typing import List

from monitor_object import MonitorObject


def get_monitor_list_json() -> str:
    return convert_monitors_list_to_json(_monitors)


def save_monitors_to_file() -> None:
    with open("monitors_data.json", "w") as file:
        json_data = convert_monitors_list_to_json(_monitors)
        file.write(json_data)
        print("Saved monitors to file")


def update_monitors_list_from_loca_json_file() -> None:
    global _monitors
    _monitors = read_monitors_list_from_file()


def read_monitors_json_from_file() -> str:
    with open("monitors_data.json", "r") as file:
        return file.read()


def read_monitors_list_from_file() -> List[MonitorObject]:
    return convert_monitors_json_to_list(read_monitors_json_from_file())


def append_monitor(monitor: MonitorObject) -> None:
    _monitors.append(monitor)
    save_monitors_to_file()


def create_and_append_monitor(title: str, url: str, test_interval_in_seconds: int) -> MonitorObject:
    new_monitor = MonitorObject(title, url, test_interval_in_seconds)
    append_monitor(new_monitor)


def remove_monitor(monitor: MonitorObject) -> None:
    _monitors.remove(monitor)
    save_monitors_to_file()


def update_monitors_from_json(monitor_data_json: str) -> None:
    """
    Rebuilds the monitors list with the data from the JSON string
    """
    global _monitors
    print("updated backend model with new data from frontend")
    _monitors = convert_monitors_json_to_list(monitor_data_json)
    save_monitors_to_file()


def convert_monitors_json_to_list(monitor_data_json: str) -> List[MonitorObject]:
    monitor_dicts = json.loads(monitor_data_json)
    # Convert test_interval_in_seconds to integer
    for monitor in monitor_dicts:
        monitor["test_interval_in_seconds"] = int(monitor["test_interval_in_seconds"])
    return [MonitorObject(**monitor_dict) for monitor_dict in monitor_dicts]


def convert_monitors_list_to_json(monitor_data_list: List[MonitorObject]) -> str:
    monitor_dicts = [monitor.__dict__ for monitor in monitor_data_list]
    return json.dumps(monitor_dicts)


_monitors: List[MonitorObject] = read_monitors_list_from_file()
