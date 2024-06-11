import gui
import system_tray
from gui import main_window
from monitor_object import MonitorObject

if __name__ == "__main__":
    # system_tray.initialize_system_tray()
    # main_window.start()

    # Debugging
    test_monitor = MonitorObject("Test Monitor", "http://exampdddddddle.com", 60)
    test_monitor.execute_test_if_due()
    print(test_monitor)

    test_monitor2 = MonitorObject("Test Monitor", "http://example.com", 60)
    test_monitor2.execute_test_if_due()
    print(test_monitor2)
