from flask import Flask, request, make_response

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
   <meta charset="UTF-8">
   <title>Title</title>
</head>
<body>
   {user_input}
</body>
</html>
"""

@app.route("/")
def index():
    user_input = request.args.get("input", "Привет, мир!")
    html = HTML_TEMPLATE.format(user_input=user_input)
    response = make_response(html)
    response.headers["Content-Security-Policy"] = "script-src 'self'"  # Запрет инлайн-скриптов
    return response

if __name__ == "__main__":
    app.run(debug=True)