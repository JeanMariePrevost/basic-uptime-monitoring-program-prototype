import monitoring_manager
import queue_manager
import system_tray
from gui import main_window

if __name__ == "__main__":
    system_tray.initialize_system_tray()
    monitoring_manager.read_monitors_list_from_file()
    print("Debug - automatic monitoring starting...")
    monitoring_manager.start_monitoring()

    queue_manager.enqueue_task(main_window.start)

    queue_manager.main_loop()
