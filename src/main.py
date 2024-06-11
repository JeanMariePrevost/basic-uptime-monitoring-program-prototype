import gui
import monitoring_manager
import system_tray
from gui import main_window
from monitor_object import MonitorObject

if __name__ == "__main__":
    # system_tray.initialize_system_tray()
    monitoring_manager.read_monitors_list_from_file()
    main_window.start()
