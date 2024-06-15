import time

import webview

import monitoring_manager
from gui import new_monitor_dialog
from util import escape_json_for_javascript


class Api:
    def __init__(self):
        self.message = "Welcome!"

    def send_monitors_data_to_backend(self, monitorDataJson) -> None:
        """
        This function is called from the frontend when the user clicks the "Apply" button
        It updates the info in the backend
        :param monitorDataJson: The JSON string containing the monitors data
        """
        print("The frontend sent this to the backend:")
        print(monitorDataJson)
        monitoring_manager.update_monitors_from_json(monitorDataJson)

    def on_new_monitor_button_clicked(self) -> None:
        print("New monitor button clicked")
        _window.evaluate_js("disableWindow()")
        new_monitor_dialog.run_dialog(self.on_new_monitor_dialog_closed)

    def on_new_monitor_dialog_closed(self, user_input) -> None:
        print(f"New monitor dialog closed with user input: {user_input}")
        _window.evaluate_js("enableWindow()")

        if user_input is not None:
            monitoring_manager.create_and_append_monitor(user_input["title"], user_input["url"], user_input["test_interval_in_seconds"])
            sendMonitorsDataToFrontend()

    def on_check_status_button_clicked(self, monitorTitle: str) -> None:
        print("Check status button clicked")
        print(monitorTitle)
        monitor = monitoring_manager.get_monitor_by_title(monitorTitle)
        monitor.execute_test()  # Currently synchronous, so really a bad idea, but simple for the prototype
        sendMonitorsDataToFrontend()


_window: webview.Window


def sendMonitorsDataToFrontend():
    monitor_data_json = escape_json_for_javascript(monitoring_manager.get_monitor_list_json())
    print(f"Sending this to the frontend: {monitor_data_json}")
    _window.evaluate_js(f'receiveMonitorsDataFromBackend("{monitor_data_json}")')


def start():
    print("main_window GUI starting...")

    # Set up pywebview
    api = Api()
    global _window
    _window = webview.create_window("BUMP - Dashboard", "gui/webgui/main_window.html", text_select=True, js_api=api, width=1200, height=800)

    # Create a function that will be called when the window is loaded
    def on_loaded():
        sendMonitorsDataToFrontend()

    # Start the webview, showing the window
    webview.start(on_loaded, debug=True)  # debug=True opens the inspector
