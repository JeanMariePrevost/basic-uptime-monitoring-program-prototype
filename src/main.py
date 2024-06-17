"""
Main entry point of the application. 
"""

import os
import sys

import monitoring_manager
from my_logger import general_logger
import queue_manager
import system_tray
from gui import main_window


import os


def resource_path(relative_path):
    """
    Get absolute path to resource, enabling PyInstaller compatibility.
    :param relative_path: The relative path to the resource
    :return: The absolute path to the resource
    """
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def exit_application():
    """
    Exits the application.
    """
    general_logger.info("Exiting application.")
    monitoring_manager.stop_monitoring()
    system_tray.stop()
    os._exit(0)


if __name__ == "__main__":
    general_logger.info("Application launched.")
    system_tray.initialize_system_tray()
    general_logger.debug("System tray initialized.")
    monitoring_manager.read_monitors_list_from_file()
    monitoring_manager.start_monitoring()

    general_logger.debug("Queuing main_window.start().")
    queue_manager.enqueue_task(main_window.start)

    general_logger.debug("Entering queue_manager.main_loop().")
    queue_manager.main_loop()
