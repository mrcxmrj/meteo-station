from client.app import App


class Router:
    def __init__(self, app_ui: App) -> None:
        self.server_socket = None
        self.app_ui = app_ui

    def route(self, method: str, route: str):
        print(f"Routing: {method}{route}")
        if route == "/":
            if method == "GET":
                return self.get_index()
        if route == "/options":
            if method == "GET":
                return self.get_options()
        elif route == "/clear-db":
            if method == "POST":
                print("POST /clear-db")
        else:
            print("Routing error: no route matched")

    def get_index(self):
        return self.app_ui.render("table")

    def get_options(self):
        return self.app_ui.generate_options_template()
