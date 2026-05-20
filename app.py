from flask import Flask, send_from_directory

app = Flask(__name__, static_folder=".", static_url_path="")


@app.route('/')
def inicio():
    return send_from_directory('.', 'index.html')


@app.route('/login')
def login():
    return send_from_directory('.', 'login.html')


@app.route('/quiz')
def quiz():
    return send_from_directory('.', 'quiz.html')


if __name__ == '__main__':
    app.run(debug=True)
