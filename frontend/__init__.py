import flet as ft
from dotenv import load_dotenv

import frontend.views as views
from frontend.backend import AgendaPlusAPI
from frontend.router import Router


def main(page: ft.Page) -> None:
    # Load .env files
    load_dotenv('.env.shared')
    load_dotenv('.env.frontend')

    router = Router(page)
    router.routes = {
        '/': views.home,
        '/cadastro': views.cadastro,
        '/compromissos': views.compromissos,
        '/calendario': views.calendario,
        '/contatos': views.contatos,
    }

    # Setup back-end API
    api = AgendaPlusAPI()
    router.set_data('api', api)

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
