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
        
    body = FormLayout([
        InputField('E-mail'),
        InputField('Senha'),
        ElevatedButton(text="Entrar",width=250,height=50.7,bgcolor="#00FFA3", on_click=lambda _: page.go("/userHome"))
    ], 'Primeira vez?', 'Registre-se', page, 'cadastro')

    view.controls.append(body)
      ## view.controls.append(ft.ElevatedButton("Dizer oi", on_click=send_name))
   
    
    # Return the view
    return view

def hello(page: ft.Page) -> ft.View:
    # Create the view
    
    
    view = ft.View()

    # Add elements
   

    # Return the view
    return view

##ft.app(name=agenda, target=home)

def cadastro(page: ft.Page) -> ft.View:
    view = ft.View()
    view.bgcolor= bgColor
    body = FormLayout([
        InputField('Nome'),
        InputField('E-mail'),
        InputField('Senha'),
        ElevatedButton(text="Criar conta",width=250,height=50.7,bgcolor="#00FFA3")
    ], 'Já tem conta?', 'Clique aqui', page, '')
    view.controls.append(body)
    return view

 
def userHome(page: ft.Page) -> ft.View:
    userDados = {
        'id': 0,
        'name': 'Rennê',
        'email': 'renne@dugrau.com'
    }
    view = ft.View()
    
    auth_layout(view, userDados, bgColor)
    
    body = Container(
        Stack([
            Container(
                Column(
                    [
                        Container(
                            Row(
                                [
                                    Text("Lista de Compromissos", weight='bold', size = 40),
                                    Container(
                                        ft.Icon(ft.icons.SEARCH, color='black'),
                                        padding = padding.all(10),
                                        margin = margin.all(10),
                                        bgcolor = 'white',
                                        border_radius = 40,
                                        width = 45,
                                        alignment = alignment.center
                                    ),
                                ],
                                alignment = ft.MainAxisAlignment.SPACE_BETWEEN
                            ),  
                            margin = margin.only(bottom=25),
                        ),
                        Container(
                            Column(
                                [
                                    Container(
                                        Text("item", size = 25),
                                        margin = margin.only(bottom=5),
                                        padding = padding.only(top = 10, bottom = 15, left= 30),
                                        alignment = alignment.center_left,
                                        bgcolor = '#C8EAF9',
                                        border_radius = 40
                                    ),
                                    Container(
                                        Text("item", size = 25),
                                        margin = margin.only(bottom=5),
                                        alignment = alignment.center_left,
                                        padding = padding.only(top = 10, bottom = 15, left= 30),
                                        
                                        bgcolor = '#C8EAF9',
                                        border_radius = 40
                                    ),
                                ],
                                alignment = ft.MainAxisAlignment.CENTER
                            ),
                            
                        ),
                    ],
                ),
                margin = margin.only(left=100, right=100),
            ),
        ],
        
    ), )
    view.controls.append(body)
    return view

