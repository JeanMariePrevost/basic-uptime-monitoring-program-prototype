import json
from dataclasses import dataclass

import webview

import monitoring_manager


class Api:
    def __init__(self):
        pass

    def on_cancel_button_clicked(self) -> None:
        print("Cancel button clicked")
        _callback_function(None)
        _window.destroy()

    def on_form_submit(self, submitted_json) -> None:
        print("Form submitted")
        print(submitted_json)
        submitted_data = json.loads(submitted_json)

        print(submitted_data["title"])
        print(submitted_data["url"])
        print(submitted_data["test_interval_in_seconds"])

        _callback_function(submitted_data)
        _window.destroy()


_window: webview.Window
_callback_function: callable


def run_dialog(callback_with_results: callable) -> str:
    global _callback_function
    _callback_function = callback_with_results
    # Set up pywebview
    api = Api()
    global _window
    _window = webview.create_window("Create New Monitor", "gui/webgui/new_monitor_dialog.html", text_select=True, js_api=api, width=700, height=390, on_top=True)

    def on_loaded():
        pass

    # Start the webview, showing the window
    webview.start(on_loaded)  # debug=True opens the inspector
