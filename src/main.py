"""
Main entry point of the application. 
"""

import monitoring_manager
from my_logger import general_logger
import queue_manager
import system_tray
from gui import main_window

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
