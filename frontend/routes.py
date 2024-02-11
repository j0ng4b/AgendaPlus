import frontend.views as views

# Define view routes
routes = {
    '/': views.home,
    '/cadastro': views.cadastro,
    '/hello/:name': views.hello,
}

