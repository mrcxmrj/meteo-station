class Router:
    # routes: dict[str, Callable]
    def __init__(self, routes) -> None:
        self.routes = routes
        pass

    def route(self, method: str, route: str):
        key = method + route
        try:
            self.routes[key]()
        except KeyError:
            print("Routing error: no route matched")
