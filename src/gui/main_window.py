import json

import webview


class Api:
    def __init__(self):
        self.message = "Welcome!"

    def sendMonitorsDataToBackend(self, monitorDataJson) -> None:
        """
        This function is called from the frontend when the user clicks the "Send data to backend" button
        :param value:
        :return:
        """
        print("The frontend sent this to the backend:")
        print(monitorDataJson)


def start():
    print("main_window GUI starting...")
    api = Api()
    window = webview.create_window("Hello PyWebView", "gui/webgui/main_window.html", text_select=True, js_api=api, width=1000, height=800)

    def on_loaded():
        dummy_monitor_data = [
            {"title": "Monitor 1", "url": "http://example1.com", "status": "up"},
            {"title": "Monitor 2", "url": "http://example2.com", "status": "down"},
            {"title": "Monitor 3", "url": "http://example3.com", "status": "unknown"},
        ]
        dummy_data_as_json = json.dumps(dummy_monitor_data)
        # Escape the JSON string properly otherwise it will break the JS
        dummy_data_as_json = dummy_data_as_json.replace('"', '\\"')
        # Send the data to the gui
        window.evaluate_js(f'receiveDataFromBackendTest("{dummy_data_as_json}")')

    webview.start(on_loaded, debug=True)  # debug=True opens the inspector
