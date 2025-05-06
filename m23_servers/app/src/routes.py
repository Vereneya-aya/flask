import json

class SimpleWSGIApp:
    def __init__(self):
        self.routes = {}

    def route(self, path):
        def decorator(func):
            self.routes[path] = func
            return func
        return decorator

    def __call__(self, environ, start_response):
        path = environ.get('PATH_INFO', '/')
        handler = self.routes.get(path)

        if handler:
            response_body = handler()
            status = '200 OK'
        else:
            response_body = json.dumps({'error': 'Not found'}, indent=4)
            status = '404 Not Found'

        headers = [('Content-type', 'application/json')]
        start_response(status, headers)
        return [response_body.encode()]

app = SimpleWSGIApp()

@app.route('/hello')
def hello():
    return json.dumps({'response': 'Hello, world!'}, indent=4)


@app.route('/hello/<name>')
def hello_username(name):
    return json.dumps({'response': f'Hello, {name}!'}, indent=4)