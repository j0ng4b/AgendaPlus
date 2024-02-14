import flet as ft
from flet import Text, Container, Column, Row, Stack, margin, alignment, TextField, ElevatedButton, Image, border, MainAxisAlignment, padding


from .components.inputField import InputField 
from .components.itemList import ItemList 
from .layouts.form_layout import FormLayout
from .layouts.auth_layout import auth_layout

bgColor = "#0CA6E9"


def home(page: ft.Page, **kwargs) -> ft.View:
    # Create the view
    view = ft.View()
    
   # view.vertical_alignment=ft.MainAxisAlignment.CENTER
    view.bgcolor= bgColor
    def send_cadastro(event):
        page.go(f'/hello/{field.value}')

    # Add elements
    view.controls.append(ft.AppBar(title=ft.Text("Flet app"), bgcolor=ft.colors.SURFACE_VARIANT))

    field = ft.TextField(label='Seu nome') # Get user input
    view.controls.append(field)
    view.controls.append(ft.ElevatedButton("Dizer oi", on_click=send_name))

    # Return the view
    return view


def hello(page: ft.Page) -> ft.View:
    # Create the view
    
    
    view = ft.View()

    # Add elements
   

    # Return the view
    return view

