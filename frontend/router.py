import re
import repath
from typing import Any, Callable

import flet as ft


class Router:
    def __init__(self, page: ft.Page) -> None:
        self.page = page
        self.routes = {}
        self.data = {}

    def add_route(self, route: str, view: Callable) -> None:
        self.routes[route] = view

    def set_data(self, key: str, value: Any) -> None:
        self.data[key] = value

    def get_data(self, key: str) -> Any:
        return self.data[key]

    def route_change(self, route: str) -> None:
        self.page.route = route
        self.__route_changed(ft.RouteChangeEvent('change:' + route))
        self.page.update()

    def route_forward(self, route: str) -> None:
        self.page.route = route
        self.__route_changed(ft.RouteChangeEvent('forward:' + route))
        self.page.update()

    def route_backward(self) -> None:
        self.page.route = self.page.views[-2].route
        self.__route_changed(
            ft.RouteChangeEvent('backward:' + self.page.route)
        )
        self.page.update()

    def view_poped(self, event: ft.ViewPopEvent) -> None:
        self.route_backward()

    def __route_changed(self, event: ft.RouteChangeEvent) -> None:
        action: str = event.route.split(':')[0]

        if action == 'change':
            if len(self.page.views) > 0:
                self.page.views.pop()
        elif action == 'forward':
            pass  # do nothing
        elif action == 'backward':
            if len(self.page.views) > 0:
                self.page.views.pop()
            return

        # Process routes
        match = None
        for route, view in self.routes.items():
            # Try match the route using repath
            # See: https://github.com/nickcoutsos/python-repath#parameters
            match = re.match(repath.pattern(route), self.page.route)

            if match:
                self.page.views.append(view(self, self.page,
                                            **match.groupdict()))

                # If matches one route others won't matched
                break

        if not match:
            raise NotImplementedError(
                f'view for route {self.page.route} not found'
            )
