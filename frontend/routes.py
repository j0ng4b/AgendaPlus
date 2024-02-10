import frontend.views as views

# Define view routes
routes = {
    '/': views.home,
    '/hello/:name': views.hello,
}

