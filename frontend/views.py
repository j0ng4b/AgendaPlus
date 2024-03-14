import flet as ft
from flet import ElevatedButton


from frontend.components.input_field import InputField
from frontend.components.item_list_commit import ItemListCommit
from frontend.components.shortly import Shortly
from frontend.layouts.form_layout import FormLayout
from frontend.layouts.auth_layout import Auth
from frontend.router import Router

bgColor = "#0CA6E9"


def home(router: Router, page: ft.Page) -> ft.View:
    view = ft.View()

    view.bgcolor = bgColor

    body = FormLayout([
        InputField('E-mail'),
        InputField('Senha', True),
        ElevatedButton(
            text="Entrar",
            width=250,
            height=50.7,
            bgcolor="#00FFA3",
            on_click=lambda _: router.route_forward("/compromissos"))
    ], 'Primeira vez?', 'Registre-se', router, 'cadastro')

    view.controls.append(body)
    return view


def cadastro(router: Router, page: ft.Page) -> ft.View:
    view = ft.View()

    view.bgcolor = bgColor

    body = FormLayout([
        InputField('Nome'),
        InputField('E-mail'),
        InputField('Senha', True),
        ElevatedButton(
            text="Criar conta",
            width=250,
            height=50.7,
            bgcolor="#00FFA3")
    ], 'Já tem conta?', 'Clique aqui', router, '')

    view.controls.append(body)
    return view


userDados = {
    'id': 0,
    'name': 'Rennê',
    'email': 'renne@dugrau.com'
}


def compromissos(router: Router, page: ft.Page) -> ft.View:
    listItem = [
        {
            'id': 0,
            'item': 'Ir para a academia',
        },
        {
            'id': 1,
            'item': 'Tocar violão',
        },
        {
            'id': 2,
            'item': 'Ir ao mercado',
        },
        {
            'id': 3,
            'item': 'Aproveitar a universidade',
        },
        {
            'id': 4,
            'item': 'Estudar TC',
        },
        {
            'id': 5,
            'item': 'Estudar TEP',
        }
    ]

    def returnItemCommit(listItem):
        itemsComponent = []
        for item in listItem:
            if item['id'] % 2 == 0:
                itemsComponent.append(ItemListCommit(item['item'], '#C8EAF9'))
            else:
                itemsComponent.append(ItemListCommit(item['item'], '#98CCE3'))

        return itemsComponent

    view = ft.View()

    body = Auth(view, userDados, bgColor, router, ft.Column(
            returnItemCommit(listItem),
            alignment=ft.MainAxisAlignment.CENTER
        ), [
            ft.Text('Lista de compromissos', weight='bold', size=40),
            ft.Container(
                ft.Icon(ft.icons.SEARCH, color='black'),
                padding=ft.padding.all(10),
                margin=ft.margin.all(10),
                bgcolor='white',
                border_radius=40,
                width=45,
                alignment=ft.alignment.center
            ),]
        )
    view.controls.append(body)
    return view


def calendario(router: Router, page: ft.Page) -> ft.View:
    view = ft.View()
    body = Auth(view, userDados, bgColor, router, ft.Column([Shortly()],
                alignment=ft.MainAxisAlignment.CENTER), [])
    view.bgcolor = '#191F26'
    view.controls.append(body)
    return view


def contatos(router: Router, page: ft.Page) -> ft.View:
    view = ft.View()
    body = Auth(view, userDados, bgColor, router, ft.Column([
        Shortly(),
    ],

        alignment=ft.MainAxisAlignment.CENTER
    ), [])
    view.bgcolor = '#191F26'
    view.controls.append(body)
    return view
