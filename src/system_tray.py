"""
THis module uses pystray to create a system tray icon and allow the program to keep running in the background
"""

import PIL.Image
import pystray

import queue_manager
from gui import main_window
from my_logger import general_logger


# Define actions for the RMB menu of the tray icon
def on_clicked_exit(icon, item):
    general_logger.debug(f'system_tray.on_clicked_exit: Clicked "{item}"')
    icon.stop()
    main_window.close()
    queue_manager.enqueue_task(lambda: exit(0))


# Define actions for the RMB menu of the tray icon
def on_clicked_open_gui(icon, item):
    general_logger.debug(f'system_tray.on_clicked_open_gui: Clicked "{item}"')
    queue_manager.enqueue_task(main_window.start)


def initialize_system_tray() -> None:
    general_logger.debug("system_tray.initialize_system_tray: Initializing system tray...")
    # Load the image for the icon
    image = PIL.Image.open("icon_32px.png")

    # Set up pystray
    icon = pystray.Icon(
        "Bump - Web Monitoring Tool",
        image,
        menu=pystray.Menu(
            pystray.MenuItem("default", on_clicked_open_gui, default=True, visible=False),  # default=True means that this is also the action that gets called when LMB the icon
            pystray.MenuItem("Exit", on_clicked_exit),
        ),
    )

    # Run pystray
    icon.run_detached()
