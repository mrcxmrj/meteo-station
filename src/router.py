import json

from ui_manager import UIManager


class Router:
    def __init__(self, ui_manager: UIManager) -> None:
        self.ui_manager = ui_manager

    def route(
        self, method: str, full_route: str, x_no_refresh: bool
    ) -> tuple[int, str, str, str]:
        print(f"Routing: {method}{full_route}")
        route = full_route.split("/")[1:]
        # if route[-1] starts with "?" == params
        if "js" in route:
            route = route[route.index("js") :]
            print(f"Rerouting to {"/".join(route)}")

        if route[0] == "" and method == "GET":
            return self.handle_get(self.ui_manager.get_app_template(page="index"))

        if route[0] == "tables" and method == "GET":
            template = (
                self.ui_manager.get_table_container_template()
                if x_no_refresh
                else self.ui_manager.get_app_template(page="tables")
            )
            return self.handle_get(template)

        if route[0] == "table" and method == "GET":
            return self.handle_get(self.ui_manager.get_table_template(route[1]))

        if route[0] == "charts" and method == "GET":
            try:
                category = route[1]
            except:
                category = ""
            # template = (
            #     self.ui_manager.get_chart_container_template(subpage)
            #     if x_no_refresh
            #     else self.ui_manager.get_app_template(page="charts", subpage=subpage)
            # )
            return self.handle_get(
                self.ui_manager.get_app_template(page="charts", subpage=category)
            )

        if route[0] == "options" and method == "GET":
            template = (
                self.ui_manager.get_table_container_template()
                if x_no_refresh
                else self.ui_manager.get_app_template(page="options")
            )
            return self.handle_get(self.ui_manager.get_app_template(page="options"))

        if route[0] == "data" and method == "GET":
            try:
                category = route[1]
            except:
                category = "temperature"
            json_data = json.dumps(self.ui_manager.get_chart_data(category))
            return self.handle_get(json_data, "json")

        if route[0] == "clear-db" and method == "POST":
            return self.handle_post(
                "Database cleared successfully", "Error clearing database"
            )

        if route[0] == "js" and method == "GET":
            try:
                with open(f"client/js/{route[1]}", "r") as f:
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
            if type == "html":
                return (
                    500,
                    "Internal Server Error",
                    "text/html",
                    "<p>Internal Server Error: Something went wrong :/</p>",
                )
            else:
                return (
                    500,
                    "Internal Server Error",
                    "text/json",
                    json.dumps({"message": "Internal Server Error"}),
                )

    def handle_post(
        self, message: str, error_message: str
    ) -> tuple[int, str, str, str]:
        try:
            return (200, "OK", "text/json", json.dumps({"message": message}))
        except:
            return (
                500,
                "Internal Server Error",
                "text/json",
                json.dumps({"message": error_message}),
            )
