from flask import Flask, render_template, request, send_from_directory
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

clientes_conectados = {} 

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/logo')
def logo():
    return send_from_directory('static', 'logo.png')

@app.route('/flaticon')
def icon():
    return send_from_directory('static', 'icon.png')

@socketio.on('connect')
def handle_connect():
    print('Cliente conectado')

@socketio.on('disconnect')
def handle_disconnect():
    nickname = [nickname for nickname, sid in clientes_conectados.items() if sid == request.sid][0]
    print(f'{nickname} desconectou-se.')
    emit('message', f'{nickname} saiu do chat.', broadcast=True)
    del clientes_conectados[nickname]

@socketio.on('register')
def handle_register(nickname):
    clientes_conectados[nickname] = request.sid
    print(f'{nickname} conectou-se ao chat.')
    emit('message', f'{nickname} entrou no chat.', broadcast=True)

@socketio.on('message')
def handle_message(message):
    nickname = [nick for nick, sid in clientes_conectados.items() if sid == request.sid][0]
    print(f'Mensagem de {nickname}: {message}')
    emit('broadcast_message', {'msg': message, 'nickname': nickname}, broadcast=True)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8881, debug=True)
