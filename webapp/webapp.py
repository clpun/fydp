from flask import Flask, render_template
from flask.ext.socketio import SocketIO, emit

app = Flask(__name__)
sockets = SocketIO(app)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/webSoc', methods=['GET'])
def web_soc_fun():
    return render_template('websocket.html')

@sockets.on('request', namespace='/api')
def test_message(message):
    print 'received: %s' % message
    for i in range(1, 10):
        emit('response', {'data': [21, 22, 53, 78, 45]})
    return

@sockets.on('disconnect', namespace='/api')
def test_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    sockets.run(app)
