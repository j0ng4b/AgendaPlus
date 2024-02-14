import flet as ft
from flet import Container

class ItemListCommit(ft.UserControl):
    
    def __init__(self, item, color):
        super().__init__()
            
        self.body = [
            Container(
                ft.Text(item, size=25),
                margin=ft.margin.only(bottom=5),
                padding=ft.padding.only(top=10, bottom=15, left=30),
                alignment=ft.alignment.center_left,
                bgcolor=color,
                border_radius=40
            ),
        ]
    
    def build(self):
        return self.body
    
    