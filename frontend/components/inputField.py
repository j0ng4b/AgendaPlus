import flet as ft
from flet import TextField, TextStyle

class InputField(ft.UserControl):
    def __init__(self, hint_text):
        super().__init__()
        self.body = TextField(
            hint_text=hint_text,
            width=250,
            border_radius = 40,
            bgcolor="#FFFFFF",
            border_width=0.5,
            border_color="#000000",
            height=60, 
            hint_style=TextStyle(color='black'),
            text_style=TextStyle(size=14,weight='w400')
        )
  
    def build(self):
        return self.body