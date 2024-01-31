import views

# Define view routes
routes = {
    '/': views.home,
    '/hello/:name': views.hello,
}

