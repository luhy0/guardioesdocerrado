from flask import Flask, send_from_directory, request, session, jsonify, redirect
import os

import firebase_admin
from firebase_admin import credentials, auth as admin_auth, firestore

app = Flask(__name__, static_folder='.', static_url_path='')
app.secret_key = 'guardioes-secret-key'

# Equivalente ao SDK enviado:
# var admin = require("firebase-admin");
# var serviceAccount = require("path/to/serviceAccountKey.json");
# admin.initializeApp({ credential: admin.credential.cert(serviceAccount) });
SERVICE_ACCOUNT_PATH = os.getenv('FIREBASE_SERVICE_ACCOUNT', 'serviceAccountKey.json')

if not firebase_admin._apps:
    cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
    firebase_admin.initialize_app(cred)

db = firestore.client()


def verify_id_token(id_token: str):
    return admin_auth.verify_id_token(id_token)


def ensure_user_document(decoded):
    uid = decoded.get('uid')
    if not uid:
        return None

    user_ref = db.collection('usuarios').document(uid)
    snap = user_ref.get()
    if not snap.exists:
        user_ref.set({
            'uid': uid,
            'nome': decoded.get('name') or decoded.get('email', 'Guardião'),
            'email': decoded.get('email', ''),
            'pontos': 1250,
            'nivel': 4,
            'missoes': 12,
            'medalhas': 5,
        })
    return user_ref.get().to_dict()


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
        decoded = verify_id_token(token)
        profile = ensure_user_document(decoded)
        session['uid'] = decoded.get('uid')
        session['email'] = decoded.get('email', '')
        session['name'] = (profile or {}).get('nome') or decoded.get('name') or decoded.get('email', 'Guardião')
        return jsonify({'ok': True})
    except Exception as exc:
        return jsonify({'ok': False, 'error': f'Falha ao validar sessão: {exc}'}), 500


@app.route('/session-logout', methods=['POST'])
def session_logout():
    session.clear()
    return jsonify({'ok': True})


@app.route('/me')
def me():
    uid = session.get('uid')
    if not uid:
        return jsonify({'ok': False}), 401

    profile = db.collection('usuarios').document(uid).get().to_dict() or {}
    return jsonify({
        'ok': True,
        'uid': uid,
        'name': profile.get('nome', session.get('name', 'Guardião')),
        'email': profile.get('email', session.get('email', '')),
        'pontos': profile.get('pontos', 0),
        'nivel': profile.get('nivel', 1),
        'missoes': profile.get('missoes', 0),
        'medalhas': profile.get('medalhas', 0),
    })


if __name__ == '__main__':
    app.run(debug=True)
