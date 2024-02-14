import frontend.views as views

# Define view routes
routes = {
    '/': views.home,
    '/cadastro': views.cadastro,
    '/userHome': views.userHome,
    '/hello/:name': views.hello,
}
