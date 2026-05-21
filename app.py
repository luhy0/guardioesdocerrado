import sqlite3
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory

app = Flask(__name__, static_folder='.', static_url_path='')
app.secret_key = 'guardioes-cerrado-secret'

DB_PATH = Path(__file__).with_name('guardioes.db')


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        '''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            pontos INTEGER NOT NULL DEFAULT 0
        )
        '''
    )
    cur.execute(
        '''
        CREATE TABLE IF NOT EXISTS animais (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            imagem TEXT NOT NULL,
            pontos_necessarios INTEGER NOT NULL
        )
        '''
    )

    if cur.execute('SELECT COUNT(*) FROM animais').fetchone()[0] == 0:
        cur.executemany(
            'INSERT INTO animais (nome, imagem, pontos_necessarios) VALUES (?, ?, ?)',
            [
                ('Lobo-guará', 'https://upload.wikimedia.org/wikipedia/commons/5/58/Chrysocyon_brachyurus.jpg', 0),
                ('Tamanduá-bandeira', 'https://upload.wikimedia.org/wikipedia/commons/2/2a/Myrmecophaga_tridactyla2.jpg', 30),
                ('Ema', 'https://upload.wikimedia.org/wikipedia/commons/1/12/Rhea_americana_-Brazil-8a.jpg', 60),
                ('Onça-pintada', 'https://upload.wikimedia.org/wikipedia/commons/0/0a/Panthera_onca_at_the_Toronto_Zoo.jpg', 90),
            ],
        )

    if cur.execute('SELECT COUNT(*) FROM usuarios').fetchone()[0] == 0:
        cur.executemany(
            'INSERT INTO usuarios (nome, email, pontos) VALUES (?, ?, ?)',
            [
                ('Guardião Demo', 'demo@cerrado.com', 75),
                ('Guardião Elite', 'elite@cerrado.com', 120),
            ],
        )

    conn.commit()
    conn.close()


init_db()


@app.route('/')
@app.route('/home')
def home():
    return send_from_directory('.', 'home.html')


@app.route('/login')
def login():
    return send_from_directory('.', 'login.html')


@app.route('/quiz')
def quiz():
    return send_from_directory('.', 'quiz.html')


@app.route('/mock-login/<int:user_id>')
def mock_login(user_id):
    conn = get_conn()
    user = conn.execute('SELECT * FROM usuarios WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    if not user:
        return 'Usuário não encontrado', 404
    session['user_id'] = user['id']
    return redirect(url_for('animais'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/animais')
def animais():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))

    conn = get_conn()
    usuario = conn.execute('SELECT * FROM usuarios WHERE id = ?', (user_id,)).fetchone()
    animais_db = conn.execute('SELECT * FROM animais ORDER BY pontos_necessarios').fetchall()
    conn.close()

    cards = []
    for a in animais_db:
        desbloqueado = usuario['pontos'] >= a['pontos_necessarios']
        cards.append({
            'id': a['id'],
            'nome': a['nome'] if desbloqueado else '???',
            'imagem': a['imagem'] if desbloqueado else None,
            'pontos_necessarios': a['pontos_necessarios'],
            'desbloqueado': desbloqueado,
        })

    return render_template('animais.html', usuario=usuario, animais=cards)


if __name__ == '__main__':
    app.run(debug=True)
