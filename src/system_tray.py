"""
THis module uses pystray to create a system tray icon and allow the program to keep running in the background
"""

import PIL.Image
import pystray
from sys import exit

import main
import queue_manager
from gui import main_window
from my_logger import general_logger

_icon: pystray.Icon


# Define actions for the RMB menu of the tray icon
def on_clicked_exit(icon, item):
    general_logger.debug(f'system_tray.on_clicked_exit: Clicked "{item}"')
    main.exit_application()


def stop():
    general_logger.debug("system_tray.stop: Stopping system tray...")
    _icon.stop()


# Define actions for the RMB menu of the tray icon
def on_clicked_open_gui(icon, item):
    general_logger.debug(f'system_tray.on_clicked_open_gui: Clicked "{item}"')
    queue_manager.enqueue_task(main_window.start)


def initialize_system_tray() -> None:
    general_logger.debug("system_tray.initialize_system_tray: Initializing system tray...")
    # Load the image for the icon
    image = PIL.Image.open(main.resource_path("icon_32px.png"))

    # Set up pystray
    global _icon
    _icon = pystray.Icon(
        "Bump - Web Monitoring Tool",
        image,
        menu=pystray.Menu(
            pystray.MenuItem("default", on_clicked_open_gui, default=True, visible=False),  # default=True means that this is also the action that gets called when LMB the icon
            pystray.MenuItem("Exit", on_clicked_exit),
        ),
    )

    # Run pystray
    _icon.run_detached()
