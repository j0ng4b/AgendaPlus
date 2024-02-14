import flet as ft
from flet import Text, Container, Column, Row, margin, alignment, padding, MainAxisAlignment, Stack
from ..components.itemMenu import ItemMenu 
from ..components.btnReturnPage import BtnReturnPage 

class Auth(ft.UserControl):
    def __init__(self, view, userDados, bgColor, page, content, titleContent):
        super().__init__()
        view.bgcolor=bgColor
        view.padding=0
        view.window_resizable=False,
        view.vertical_alignment='start'
        view.horizontal_alignment='center'
        view.drawer = ft.NavigationDrawer(
            controls=[
                ft.Container(height=12),
                Container(
                    Column([
                        Container(
                            Column([
                                Container(
                                    Text(f"Olá, {userDados["name"]}", font_family="Rounded Mplus 1C Bould", size=30,color="black", weight="bold"),
                                    alignment=alignment.center, 
                                ),
                                ft.Divider(thickness=1, color="black"),
                            ]),
                        ),
                        
                        Container(
                            Column([
                                ItemMenu("Compromissos", ft.icons.CALENDAR_TODAY_OUTLINED, page, 'compromissos'),
                                ItemMenu("Calendário", ft.icons.CALENDAR_MONTH_OUTLINED, page, 'calendario'),
                                ItemMenu("Contatos", ft.icons.PERM_CONTACT_CALENDAR_OUTLINED, page, 'contatos'), 
                            ]),
                        ),
                        
                        Container(
                            Row([
                                    ft.Icon(ft.icons.LOGOUT, color='black'),
                                ], 
                                alignment=MainAxisAlignment.CENTER,
                            ),
                            on_click=lambda _:page.route_forward(''),
                            padding=padding.all(10),
                            margin=margin.all(10),
                            bgcolor='white',
                            border_radius=40,
                            width=45,
                            alignment=alignment.center_left
                        ),
                    ], alignment=MainAxisAlignment.SPACE_BETWEEN),
                    height = 650
                ),

            ],
            bgcolor='#00B2FF',
        )
        
        
        def show_drawer(e):
            view.drawer.open=True
            view.drawer.update()

        
        view.appbar = ft.AppBar(
            leading=ft.IconButton(icon="menu", on_click=show_drawer, icon_color="white"),
            leading_width=40,
            title=Text("Agenda+",font_family="Rounded Mplus 1C Bould",size=30,color="white",weight="bold"),
            center_title=True,
            bgcolor="#211C1C",
            actions=[
                BtnReturnPage(page),
            ],
        )
        self.body = Container(
            Stack([
                Container(
                    Column(
                        [
                            Container(
                                Row(
                                    titleContent,

                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                                ),  
                                margin=margin.only(bottom=25),
                            ),
                            Container(
                                content,     
                            ),
                        ],
                    ),
                    margin=margin.only(left=100, right=100),
                ),
            ],
        ), )
        
    def build(self):
        return self.body