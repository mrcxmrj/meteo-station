from ui_manager import UIManager


class Router:
    def __init__(self, ui_manager: UIManager) -> None:
        self.ui_manager = ui_manager

    def route(
        self, method: str, route: str, x_no_refresh: bool
    ) -> tuple[int, str, str, str]:
        print(f"Routing: {method}{route}")
        print(x_no_refresh)

        if route == "/" and method == "GET":
            return self.handle_get(self.ui_manager.get_app_template(page="index"))

        if route == "/table" and method == "GET":
            template = (
                self.ui_manager.get_table_container_template()
                if x_no_refresh
                else self.ui_manager.get_app_template(page="table")
            )
            return self.handle_get(template)

        if route == "/chart" and method == "GET":
            template = (
                self.ui_manager.get_table_container_template()
                if x_no_refresh
                else self.ui_manager.get_app_template(page="chart")
            )
            return self.handle_get(self.ui_manager.get_app_template(page="chart"))

        if route == "/options" and method == "GET":
            template = (
                self.ui_manager.get_table_container_template()
                if x_no_refresh
                else self.ui_manager.get_app_template(page="options")
            )
            return self.handle_get(self.ui_manager.get_app_template(page="options"))

        if route == "/clear-db" and method == "POST":
            return self.handle_post(
                "Database cleared successfully", "Error clearing database"
            )

        if route == "/js/script.js" and method == "GET":
            try:
                with open("client/js/script.js", "r") as f:
                    body = f.read()
                    return self.handle_get(body, type="js")
            except:
                print("Script not found")

        print("Routing error: no route matched or resource not found")
        return (
            404,
            "Not Found",
            "text/html",
            "<p>404: Not Found</p>",
        )

    def handle_get(self, body: str, type: str = "html") -> tuple[int, str, str, str]:
        try:
            return 200, "OK", f"text/{type}", body
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
