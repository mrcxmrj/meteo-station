class Router:
    def __init__(self) -> None:
        pass

    def route(self, method: str, route: str):
        if route == "/":
            if method == "GET":
                print("GET /")
        elif route == "/clear-db":
            if method == "POST":
                print("POST /clear-db")
        else:
            print("no route matched")
