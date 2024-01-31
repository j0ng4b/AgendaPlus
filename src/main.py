import re
import repath
import flet as ft

from routes import routes

def main(page: ft.Page) -> None:
    def route_chaged(event: ft.RouteChangeEvent) -> None:
        # Clear all views
        page.views.clear()

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

        page.update()

    def view_poped(event: ft.ViewPopEvent):
        page.views.pop()
        page.go(page.views[-1])

    page.on_route_change = route_chaged
    page.on_view_pop = view_poped

    # Go to home page
    page.go('/')

if __name__ == '__main__':
    ft.app(target=main)

