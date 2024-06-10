import json

import webview


class Api:
    def __init__(self):
        self.message = "Welcome!"

    def set_welcome_message(self, message):
        self.message = message
        return self.message

    def execute_action(self):
        print("You clicked the button")
        self.set_welcome_message("You clicked the button")
        return "Action executed"


def start():
    print("main_window GUI starting...")
    api = Api()
    window = webview.create_window("Hello PyWebView", "gui/webgui/main_window.html", text_select=True, js_api=api)

    def on_loaded():
        print("On loaded ran")
        dummy_monitor_data = [
            {"title": "Monitor 1", "url": "http://example1.com", "status": "up"},
            {"title": "Monitor 2", "url": "http://example2.com", "status": "down"},
            {"title": "Monitor 3", "url": "http://example3.com", "status": "unknown"},
        ]
        # window.evaluate_js('document.querySelector("h1").textContent = "ye"')
        dummy_data_as_json = json.dumps(dummy_monitor_data)
        print(dummy_data_as_json)
        # Escape the JSON string properly
        dummy_data_as_json = dummy_data_as_json.replace('"', '\\"')
        print(dummy_monitor_data.__repr__())  # Seems it by default represents itself as a JSON string in string form
        window.evaluate_js(f'receiveDataFromBackendTest("{dummy_data_as_json}")')

    webview.start(on_loaded, debug=True)  # Debug enables the inspector
    print("gui start() finished")
