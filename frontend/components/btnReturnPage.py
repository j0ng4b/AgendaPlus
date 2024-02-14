import flet as ft


class BtnReturnPage(ft.UserControl):
    def __init__(self, page):
        super().__init__()
        self.body = ft.Container(
            ft.Image(
                src="../assets/returnIcon.png",
                width=30,
                height=30,
            ),
            on_click=lambda _:page.route_backward(),
            margin=ft.margin.only(right=10),
        )
  
    def build(self):
        return self.body