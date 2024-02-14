import re
import repath
import flet as ft

from frontend.routes import routes


def main(page: ft.Page) -> None:
    def route_changed(event: ft.RouteChangeEvent) -> None:
        action: str = event.route.split(':')[0]

        if action == 'change':
            if len(page.views) > 0:
                page.views.pop()
        elif action == 'forward':
            pass  # do nothing
        elif action == 'backward':
            if len(page.views) > 0:
                page.views.pop()
            return

        # Process routes
        for route, view in routes.items():
            # Try match the route using repath
            # See: https://github.com/nickcoutsos/python-repath#parameters
            match = re.match(repath.pattern(route), page.route)

            if match:
                page.views.append(view(page, **match.groupdict()))

                # If matches one route others won't matched
                break

        if not match:
            raise NotImplementedError(f'view for route {page.route} not found')

    def route_change(route: str) -> None:
        page.route = route
        route_changed(ft.RouteChangeEvent('change:' + route))
        page.update()

    def route_forward(route: str) -> None:
        page.route = route
        route_changed(ft.RouteChangeEvent('forward:' + route))
        page.update()

    def route_backward() -> None:
        page.route = page.views[-2].route
        route_changed(ft.RouteChangeEvent('backward:' + page.route))
        page.update()

    def view_poped(event: ft.ViewPopEvent) -> None:
        page.route_backward()

    # Prevents to the route change event by trigged twice because route
    # manipulation is done by the route functions only
    page.on_route_change = None

    page.route_change = route_change
    page.route_forward = route_forward
    page.route_backward = route_backward

    page.on_view_pop = view_poped

    # Clear all views
    page.views.clear()

    # Go to home page
    page.route_change('/')


if __name__ == '__main__':
    ft.app(target=main)
