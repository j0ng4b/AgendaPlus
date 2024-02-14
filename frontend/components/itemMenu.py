import flet as ft
from flet import padding, Container, Row, MainAxisAlignment, margin, Text

class ItemMenu(ft.UserControl):
    
    def __init__(self, text, icon, page, route):
        super().__init__()
        def on_hover(e):
            e.control.bgcolor = 'white' if e.data == 'true' else 'black'
            hoverCheck = 'black' if e.data == 'true' else 'white'
            
            for control in e.control.content.controls:
                control.color = hoverCheck
            
            e.control.update()
            
        self.body = [
            Container(       
                Row(
                    [
                        ft.Icon(icon, color='white'),
                        Text(text, color='white', weight='bold')
                    ],
                    alignment = MainAxisAlignment.START,
                ),

                padding = padding.only(top=15, bottom=15, right=10, left=20),
                margin = margin.only(right=10, left=10, top = 5,  bottom = 10),
                border_radius=20,
                on_hover=on_hover,
                bgcolor = 'black',
                on_click=lambda _: page.route_forward(f"/{route}")
                
            ),
        ]
    
    def build(self):
        return self.body
    
    