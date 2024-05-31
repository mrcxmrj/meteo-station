from client.app import App


class Router:
    def __init__(self, app_ui: App) -> None:
        self.server_socket = None
        self.app_ui = app_ui

    def route(self, method: str, route: str) -> tuple[int, str, str, str]:
        print(f"Routing: {method}{route}")
        if route == "/":
            if method == "GET":
                return self.handle_get(self.app_ui.render("table"))
        if route == "/options":
            if method == "GET":
                return self.handle_get(self.app_ui.render("options"))
        elif route == "/clear-db":
            if method == "POST":
                print("POST /clear-db")
                return self.handle_post(
                    "Database cleared successfully", "Error clearing database"
                )

        print("Routing error: no route matched")
        return (
            404,
            "Not Found",
            "text/html",
            "<p>404: Not Found</p>",
        )

    def handle_get(self, body: str) -> tuple[int, str, str, str]:
        try:
            return 200, "OK", "text/html", body
        except:
            return (
                500,
                "Internal Server Error",
                "text/html",
                "<p>Internal Server Error: Something went wrong :/</p>",
            )

    def handle_post(
        self, message: str, error_message: str
    ) -> tuple[int, str, str, str]:
        try:
            return (
                200,
                "OK",
                "text/html",
                f'{{"message": {message}}}',
            )
        except:
            return (
                500,
                "Internal Server Error",
                "text/html",
                f'{{"message": {error_message}}}',
            )
