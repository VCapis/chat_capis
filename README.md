# Aplicação de Chat com Flask-SocketIO

Este aplicativo de chat utiliza o Flask e o Flask-SocketIO para criar uma plataforma de comunicação em tempo real. Ele suporta funcionalidades essenciais, como conectar e desconectar usuários, além de permitir a troca de mensagens entre os usuários conectados.

## Configuração Inicial

O aplicativo é inicializado com as configurações principais a seguir:

```python
from flask import Flask, render_template, request, send_from_directory
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

clientes_conectados = {}
```

- Flask(__name__): Cria uma instância da aplicação Flask.
- app.config['SECRET_KEY']: Define uma chave secreta para a aplicação, necessária para manter as sessões do cliente seguras.
- SocketIO(app): Inicializa o Flask-SocketIO, integrando-o à aplicação Flask.
- clientes_conectados = {}: Um dicionário para manter o registro dos clientes conectados.

## Funcionalidades

### Rotas do Flask

```python
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/logo')
def logo():
    return send_from_directory('static', 'logo.png')

@app.route('/flaticon')
def icon():
    return send_from_directory('static', 'icon.png')
```

- @app.route('/'): Carrega a página principal do chat.
- @app.route('/logo') e @app.route('/flaticon'): Servem arquivos estáticos, como imagens, necessários para a aplicação.

### Eventos do Socket.IO

```python
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
```

- @socketio.on('connect'): Trata da conexão de um novo cliente.
- @socketio.on('disconnect'): Gerencia a desconexão de um cliente, informando aos demais usuários.
- @socketio.on('register'): Registra um novo usuário no chat, associando um nickname ao seu ID de sessão.
- @socketio.on('message'): Lida com a recepção e transmissão de mensagens entre os usuários.


## Execução

Para rodar o servidor:

Instalar o Python 3:
```
https://www.python.org/
```

Verificar a instalação do Pyhton:
```
python --version ou python3 --version
pip --version
```

Instalar dependências:
```
pip install -U Flask
pip install flask-socketio
```

Verificar a instalação das dependências:
```
pip list
``` 

Iniciar Servidor:
```python
python server.py ou python3 server.py
```
Isso iniciará o servidor Flask-SocketIO, tornando a aplicação acessível através do endereço http://localhost:8881 ou um endereço/IP específico configurado com host='0.0.0.0' e port=8881.