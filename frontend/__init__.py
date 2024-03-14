import flet as ft

from frontend.router import Router
import frontend.views as views


def main(page: ft.Page) -> None:
    router = Router(page)

    router.routes = {
        '/': views.home,
        '/cadastro': views.cadastro,
        '/compromissos': views.compromissos,
        '/calendario': views.calendario,
        '/contatos': views.contatos,
    }

    # Prevents to the route change event by trigged twice because route
    # manipulation is done by the route functions only
    page.on_route_change = None
    page.on_view_pop = router.view_poped

    # Clear all views
    page.views.clear()

    # Go to home page
    router.route_change('/')


if __name__ == '__main__':
    ft.app(target=main)
