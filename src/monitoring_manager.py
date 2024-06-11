"""
This module is responsible for managing the monitors. It provides methods to add, remove, and update monitors.
It also provides methods to save and load the monitors to and from a file.
"""

import json
from typing import List

from monitor_object import MonitorObject

_monitors: List[MonitorObject] | None = None


def get_monitor_list() -> List[MonitorObject]:
    global _monitors
    if _monitors is None:
        _monitors = load_monitors_list_from_file()
    return _monitors


def get_monitor_list_json() -> str:
    return convert_monitors_list_to_json(get_monitor_list())


def save_monitors_to_file() -> None:
    with open("monitors_data.json", "w") as file:
        json_data = convert_monitors_list_to_json(monitors)
        file.write(json_data)


def load_monitors_list_from_file() -> List[MonitorObject]:
    try:
        with open("monitors_data.json", "r") as file:
            return convert_monitors_json_to_list(file.read())
    except FileNotFoundError:
        print("No monitor data file found. Returning empty list.")
        return []


def add_monitor(monitor: MonitorObject) -> None:
    monitors.append(monitor)
    save_monitors_to_file()


def remove_monitor(monitor: MonitorObject) -> None:
    monitors.remove(monitor)
    save_monitors_to_file()


def update_monitors_from_json(monitor_data_json: str) -> None:
    """
    Rebuilds the monitors list with the data from the JSON string
    """
    global monitors
    monitors = convert_monitors_json_to_list(monitor_data_json)
    save_monitors_to_file()


def convert_monitors_json_to_list(monitor_data_json: str) -> List[MonitorObject]:
    monitor_dicts = json.loads(monitor_data_json)
    return [MonitorObject(**monitor_dict) for monitor_dict in monitor_dicts]


def convert_monitors_list_to_json(monitor_data_list: List[MonitorObject]) -> str:
    monitor_dicts = [monitor.__dict__ for monitor in monitor_data_list]
    return json.dumps(monitor_dicts)
