import gui.main_window
import system_tray

if __name__ == "__main__":
    system_tray.initialize_system_tray()
    gui.main_window.start()
