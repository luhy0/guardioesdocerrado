from flask import Flask, send_from_directory, request, session, jsonify, redirect
import json
from urllib import request as urlrequest

app = Flask(__name__, static_folder='.', static_url_path='')
app.secret_key = 'guardioes-secret-key'
FIREBASE_API_KEY = 'AIzaSyAdPQDhJB_MDkyK_6DrBYNIDsxeIm_B3hc'


def verify_id_token(id_token: str):
    endpoint = f"https://identitytoolkit.googleapis.com/v1/accounts:lookup?key={FIREBASE_API_KEY}"
    payload = json.dumps({'idToken': id_token}).encode('utf-8')
    req = urlrequest.Request(endpoint, data=payload, headers={'Content-Type': 'application/json'})
    with urlrequest.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read().decode('utf-8'))
    users = data.get('users', [])
    return users[0] if users else None


@app.route('/')
@app.route('/index.html')
def inicio():
    return send_from_directory('.', 'index.html')


@app.route('/login')
@app.route('/login.html')
def login():
    return send_from_directory('.', 'login.html')


@app.route('/dashboard')
def dashboard():
    if not session.get('uid'):
        return redirect('/login.html')
    return send_from_directory('.', 'dashboard.html')


@app.route('/session-login', methods=['POST'])
def session_login():
    body = request.get_json(silent=True) or {}
    token = body.get('idToken')
    if not token:
        return jsonify({'ok': False, 'error': 'Token ausente'}), 400
    try:
        user = verify_id_token(token)
        if not user:
            return jsonify({'ok': False, 'error': 'Token inválido'}), 401
        session['uid'] = user.get('localId')
        session['email'] = user.get('email', '')
        session['name'] = user.get('displayName') or user.get('email', 'Guardião')
        return jsonify({'ok': True})
    except Exception:
        return jsonify({'ok': False, 'error': 'Falha ao validar sessão'}), 500


@app.route('/session-logout', methods=['POST'])
def session_logout():
    session.clear()
    return jsonify({'ok': True})


@app.route('/me')
def me():
    if not session.get('uid'):
        return jsonify({'ok': False}), 401
    return jsonify({'ok': True, 'uid': session['uid'], 'name': session.get('name', 'Guardião'), 'email': session.get('email', '')})


if __name__ == '__main__':
    app.run(debug=True)
