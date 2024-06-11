import webview

import monitoring_manager


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


def start():
    print("main_window GUI starting...")

    # Set up pywebview
    api = Api()
    window = webview.create_window("BUMP - Dashboard", "gui/webgui/main_window.html", text_select=True, js_api=api, width=1200, height=800)

    # Create a function that will be called when the window is loaded
    def on_loaded():
        # Send the data to the gui
        monitor_data_json = escape_json_for_javascript(monitoring_manager.get_monitor_list_json())
        print("Going to send:")
        print(monitor_data_json)
        window.evaluate_js(f'receiveMonitorsDataFromBackend("{monitor_data_json}")')

    # Start the webview, showing the window
    webview.start(on_loaded, debug=True)  # debug=True opens the inspector


def escape_json_for_javascript(json_string: str):
    monitor_data_json = json_string.replace('"', '\\"')
    return monitor_data_json
