import gui
import monitoring_manager
import system_tray
from gui import main_window, new_monitor_dialog
from monitor_object import MonitorObject

if __name__ == "__main__":
    # system_tray.initialize_system_tray()
    monitoring_manager.read_monitors_list_from_file()
    main_window.start()
    # new_monitor_dialog.run_dialog(lambda user_input: print(f"user_input: {user_input}"))
