import flet as ft


class Shortly(ft.UserControl):
    def __init__(self):
        super().__init__()

        self.body = [
            ft.Container(
                ft.Column([
                    ft.Image(src='../assets/loading.gif'),
                ], alignment=ft.MainAxisAlignment.CENTER),
                alignment=ft.alignment.center
            ),
        ]

    def build(self):
        return self.body
