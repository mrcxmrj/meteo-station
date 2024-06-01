from client.app import App


class Router:
    def __init__(self, app_ui: App) -> None:
        self.app_ui = app_ui

    def route(self, method: str, route: str) -> tuple[int, str, str, str]:
        print(f"Routing: {method}{route}")
        if route == "/" and method == "GET":
            return self.handle_get(self.app_ui.render(page="index"))
        if route == "/table" and method == "GET":
            return self.handle_get(self.app_ui.render(page="table"))
        if route == "/chart" and method == "GET":
            return self.handle_get(self.app_ui.render(page="chart"))
        if route == "/options" and method == "GET":
            return self.handle_get(self.app_ui.render(page="options"))
        if route == "/clear-db" and method == "POST":
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
