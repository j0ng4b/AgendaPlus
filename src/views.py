import flet as ft

def home(page: ft.Page, **kwargs) -> ft.View:
    # Create the view
    view = ft.View()

    def send_name(event):
        page.go(f'/hello/{field.value}')

    # Add elements
    view.controls.append(ft.AppBar(title=ft.Text("Flet app"), bgcolor=ft.colors.SURFACE_VARIANT))

    field = ft.TextField(label='Seu nome') # Get user input
    view.controls.append(field)
    view.controls.append(ft.ElevatedButton("Dizer oi", on_click=send_name))

    # Return the view
    return view

def hello(page: ft.Page, name) -> ft.View:
    # Create the view
    view = ft.View()

    # Add elements
    view.controls.append(ft.Text(value=f'hello {name}'))

    # Return the view
    return view

