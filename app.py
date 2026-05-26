from flask import Flask, send_from_directory

app = Flask(__name__, static_folder='.', static_url_path='')


@app.route('/')
@app.route('/index.html')
def inicio():
    return send_from_directory('.', 'index.html')


@app.route('/login')
@app.route('/login.html')
def login():
    return send_from_directory('.', 'login.html')


if __name__ == '__main__':
    app.run(debug=True)
