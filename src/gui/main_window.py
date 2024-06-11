import json

import webview

import monitoring_manager


class Api:
    def __init__(self):
        self.message = "Welcome!"

    def sendMonitorsDataToBackend(self, monitorDataJson) -> None:
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

    print("Loading monitor data from file...")
    monitor_data_json = monitoring_manager.get_monitor_list_json()
    if monitor_data_json is None or monitor_data_json == "" or monitor_data_json == "[]":
        print("No monitor data found in file. Creating dummy data for testing...")
        dummy_monitor_data = [
            {"title": "Monitor 1", "url": "http://example1.com", "status": "up"},
            {"title": "Monitor 2", "url": "http://example2.com", "status": "down"},
            {"title": "Monitor 3", "url": "http://example3.com", "status": "unknown"},
        ]
        monitor_data_json = json.dumps(dummy_monitor_data)

    # Escape the JSON string properly otherwise it will break the JS
    monitor_data_json = monitor_data_json.replace('"', '\\"')
    print(f"Loaded monitor data: {monitor_data_json}")

    # Set up pywebview
    api = Api()
    window = webview.create_window("Hello PyWebView", "gui/webgui/main_window.html", text_select=True, js_api=api, width=1000, height=800)

    # Create a function that will be called when the window is loaded
    def on_loaded():
        # Send the data to the gui
        window.evaluate_js(f'receiveDataFromBackendTest("{monitor_data_json}")')

    # Start the webview, showing the window
    webview.start(on_loaded, debug=True)  # debug=True opens the inspector
