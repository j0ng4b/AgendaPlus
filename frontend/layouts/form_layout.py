import flet as ft
from flet import Text, Container, Column, Row, Stack, margin, alignment, Image


class FormLayout(ft.UserControl):
    def __init__(self, listInput, textDown, linkDown, router, route):
        super().__init__()
        self.body = Container(
            Stack([
                Container(
                    Container(
                        Column([
                            Container(
                                Row([
                                    Image(
                                        src="../assets/agenda.png",
                                        width=70,
                                        height=70,
                                    ),
                                    Text("Agenda+",
                                         height=100,
                                         font_family="Rounded Mplus 1C Bould",
                                         size=60,
                                         color="#211C1C",
                                         weight="bold")],
                                    alignment=ft.MainAxisAlignment.CENTER),
                                margin=margin.only(bottom=30),
                            ),
                            Container(
                                Column(listInput,
                                       alignment=ft.MainAxisAlignment.CENTER),
                                alignment=alignment.center
                            ),
                            Container(
                                Row([
                                    Container(
                                        width=400,
                                        border=ft.border.all(0.4, ft.colors.WHITE),
                                    ),
                                    Text("ou",
                                         height=30.54,
                                         font_family="Rounded Mplus 1C Bould",
                                         size=16,
                                         color="#EDEDED",
                                         weight="bold"),
                                    Container(
                                        width=400,
                                        border=ft.border.all(0.4, ft.colors.WHITE),
                                    ),
                                ], alignment=ft.MainAxisAlignment.CENTER),
                                margin=margin.only(bottom=30, top=30)
                            ),
                            Row([
                                Text(textDown,
                                     height=54.54,
                                     font_family="Rounded Mplus 1C Bould",
                                     size=16,
                                     color="#EDEDED"),
                                Container(
                                    Text(linkDown,
                                         height=54.54,
                                         font_family="Rounded Mplus 1C Bould",
                                         size=16,
                                         color="#00FFA3"),
                                    on_click=lambda _: router.route_forward(f"/{route}")
                                ),
                            ], alignment=ft.MainAxisAlignment.CENTER),
                        ], alignment=ft.MainAxisAlignment.CENTER),
                        margin=margin.only(top=80),
                        alignment=alignment.center
                    ),
                    alignment=alignment.center
                )
            ],)
        )

    def build(self):
        return self.body
