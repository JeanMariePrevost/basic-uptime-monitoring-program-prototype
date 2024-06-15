"""
THis module uses pystray to create a system tray icon and allow the program to keep running in the background
"""

import PIL.Image
import pystray

import queue_manager
from gui import main_window


# Define actions for the RMB menu of the tray icon
def on_clicked_exit(icon, item):
    print(f'Clicked "{item}"')
    print("Going to stop pystray now...")
    print("Going to exit now...")
    icon.stop()
    exit(0)
    # TODO - Implement a single exit function somewhere, exiting everything (e.g. closing all GUI windows, stopping pystray...)


# Define actions for the RMB menu of the tray icon
def on_clicked_open_gui(icon, item):
    print(f'Clicked "{item}"')
    queue_manager.enqueue_task(main_window.start)


def initialize_system_tray() -> None:
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
