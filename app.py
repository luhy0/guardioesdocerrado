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
            ('Tamanduá-bandeira', 'https://upload.wikimedia.org/wikipedia/commons/2/2a/Myrmecophaga_tridactyla2.jpg', 30),
            ('Ema', 'https://upload.wikimedia.org/wikipedia/commons/1/12/Rhea_americana_-Brazil-8a.jpg', 60),
            ('Onça-pintada', 'https://upload.wikimedia.org/wikipedia/commons/0/0a/Panthera_onca_at_the_Toronto_Zoo.jpg', 90),
        ])
    if cur.execute('SELECT COUNT(*) FROM usuarios').fetchone()[0] == 0:
        cur.executemany('INSERT INTO usuarios (nome, email, pontos) VALUES (?, ?, ?)', [('Guardião Demo', 'demo@cerrado.com', 75), ('Guardião Elite', 'elite@cerrado.com', 120)])
    if cur.execute('SELECT COUNT(*) FROM conquistas').fetchone()[0] == 0:
        cur.executemany('INSERT INTO conquistas (nome, descricao, pontos_minimos) VALUES (?, ?, ?)', [
            ('Explorador do Cerrado', 'Alcançou 50 pontos e iniciou sua jornada de descobertas.', 50),
            ('Guardião Iniciante', 'Conquistou 100 pontos e protege as espécies do bioma.', 100),
            ('Protetor da Natureza', 'Chegou a 200 pontos e se tornou referência ambiental.', 200),
        ])
    conn.commit()
    conn.close()


def sync_user_conquistas(user_id):
    conn = get_conn()
    user = conn.execute('SELECT pontos FROM usuarios WHERE id = ?', (user_id,)).fetchone()
    if not user:
        conn.close(); return
    conquistas = conn.execute('SELECT id FROM conquistas WHERE pontos_minimos <= ?', (user['pontos'],)).fetchall()
    for c in conquistas:
        conn.execute('INSERT OR IGNORE INTO usuario_conquistas (usuario_id, conquista_id) VALUES (?, ?)', (user_id, c['id']))
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


@app.route('/mapa')
def mapa():
    return send_from_directory('.', 'mapa.html')


@app.route('/historias')
def historias():
    return send_from_directory('.', 'historias.html')


@app.route('/mock-login/<int:user_id>')
def mock_login(user_id):
    conn = get_conn()
    user = conn.execute('SELECT * FROM usuarios WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    if not user:
        return 'Usuário não encontrado', 404
    session['user_id'] = user['id']
    sync_user_conquistas(user['id'])
    return redirect(url_for('animais'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/api/quiz-result', methods=['POST'])
def quiz_result():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'não autenticado'}), 401
    points = int((request.get_json(silent=True) or {}).get('points', 0))
    points = max(points, 0)
    conn = get_conn()
    conn.execute('UPDATE usuarios SET pontos = pontos + ? WHERE id = ?', (points, user_id))
    conn.commit()
    usuario = conn.execute('SELECT * FROM usuarios WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    sync_user_conquistas(user_id)
    return jsonify({'ok': True, 'pontos': usuario['pontos']})


@app.route('/animais')
def animais():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    conn = get_conn()
    usuario = conn.execute('SELECT * FROM usuarios WHERE id = ?', (user_id,)).fetchone()
    animais_db = conn.execute('SELECT * FROM animais ORDER BY pontos_necessarios').fetchall()
    conn.close()
    cards = [{'id': a['id'], 'nome': a['nome'] if usuario['pontos'] >= a['pontos_necessarios'] else '???', 'imagem': a['imagem'] if usuario['pontos'] >= a['pontos_necessarios'] else None, 'pontos_necessarios': a['pontos_necessarios'], 'desbloqueado': usuario['pontos'] >= a['pontos_necessarios']} for a in animais_db]
    return render_template('animais.html', usuario=usuario, animais=cards)


@app.route('/conquistas')
def conquistas():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    sync_user_conquistas(user_id)
    conn = get_conn()
    usuario = conn.execute('SELECT * FROM usuarios WHERE id = ?', (user_id,)).fetchone()
    all_c = conn.execute('SELECT * FROM conquistas ORDER BY pontos_minimos').fetchall()
    unlocked_ids = {r['conquista_id'] for r in conn.execute('SELECT conquista_id FROM usuario_conquistas WHERE usuario_id = ?', (user_id,)).fetchall()}
    conn.close()
    cards = []
    for c in all_c:
        unlocked = c['id'] in unlocked_ids
        cards.append({'nome': c['nome'] if unlocked else '???', 'descricao': c['descricao'] if unlocked else 'Continue jogando para desbloquear.', 'pontos_minimos': c['pontos_minimos'], 'unlocked': unlocked})
    return render_template('conquistas.html', usuario=usuario, conquistas=cards)


@app.route('/perfil')
def perfil():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    sync_user_conquistas(user_id)
    conn = get_conn()
    usuario = conn.execute('SELECT * FROM usuarios WHERE id = ?', (user_id,)).fetchone()
    medalhas = conn.execute('''SELECT c.nome, c.descricao, c.pontos_minimos FROM usuario_conquistas uc JOIN conquistas c ON c.id = uc.conquista_id WHERE uc.usuario_id = ? ORDER BY c.pontos_minimos''', (user_id,)).fetchall()
    conn.close()
    return render_template('perfil.html', usuario=usuario, medalhas=medalhas)


if __name__ == '__main__':
    app.run(debug=True)
