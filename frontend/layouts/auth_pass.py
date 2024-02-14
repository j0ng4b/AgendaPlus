import flet as ft
from flet import Text, Container, Column, Row, margin, alignment, padding, MainAxisAlignment, Image
from ..components.itemMenu import ItemMenu
        
def auth_layout(view, userDados, bgColor, page):
    view.bgcolor=bgColor
    view.padding = 0
    view.window_resizable = False,
    view.vertical_alignment = 'start'
    view.horizontal_alignment = 'center'
    view.drawer = ft.NavigationDrawer(
        controls=[
            ft.Container(height=12),
            Container(
                Column([
                    Container(
                        Column([
                            Container(
                                Text(f"Olá, {userDados["name"]}", font_family="Rounded Mplus 1C Bould", size=30,color="black", weight="bold"),
                                alignment = alignment.center, 
                            ),
                            ft.Divider(thickness=1, color="black"),
                        ]),
                    ),
                    
                    Container(
                        Column([
                            ItemList("Compromissos", ft.icons.CALENDAR_TODAY_OUTLINED),
                            ItemList("Calendário", ft.icons.CALENDAR_MONTH_OUTLINED),
                            ItemList("Contatos", ft.icons.PERM_CONTACT_CALENDAR_OUTLINED), 
                        ]),
                    ),
                    
                    Container(
                        Row([
                                ft.Icon(ft.icons.LOGOUT, color='black'),
                            ], 
                            alignment = MainAxisAlignment.CENTER
                        ),
                        padding = padding.all(10),
                        margin = margin.all(10),
                        bgcolor = 'white',
                        border_radius = 40,
                        width = 45,
                        alignment = alignment.center_left
                    ),
                ], alignment = MainAxisAlignment.SPACE_BETWEEN),
                height = 650
            ),

        ],
        bgcolor = '#00B2FF',
    )
    
    
    def show_drawer(e):
        view.drawer.open = True
        view.drawer.update()

    
    view.appbar = ft.AppBar(
        leading=ft.IconButton(icon="menu", on_click=show_drawer, icon_color="white"),
        leading_width=40,
        title=Text("Agenda+",font_family="Rounded Mplus 1C Bould",size=30,color="white",weight="bold"),
        center_title=True,
        bgcolor="#211C1C",
        actions=[
            Container(
                Image(
                    src = "../assets/returnIcon.png",
                    width = 30,
                    height = 30,
                ),
                on_click=lambda _: page.route_backward(),
                margin = margin.only(right = 10),
            )
        ],
    )
