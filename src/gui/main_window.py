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
    window = webview.create_window("Hello PyWebView", "gui/html/index.html", js_api=api)

    def on_loaded():
        print("On loaded ran")
        window.evaluate_js(f'document.getElementById("welcome-message").innerText = "{api.message}"')

    webview.start(on_loaded)
    print("gui start() finished")
