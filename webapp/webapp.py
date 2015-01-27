from flask import Flask, render_template
from flask.ext.socketio import SocketIO, emit
from py.src import mindcraft
from py.src.test_data_generator import TestDataGenerator

app = Flask(__name__)
sockets = SocketIO(app)

data_generator = TestDataGenerator()


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/webSoc', methods=['GET'])
def web_soc_fun():
    return render_template('websocket.html')


@sockets.on('request', namespace='/api')
def get_power(message):
    for i in mindcraft.main():
        emit('response', {'data': i})


@sockets.on('request_test_data', namespace='/api')
def get_power_test_data(message):
    for response_data in data_generator.generate_data():
        print 'Sending response test data: %s' % response_data
        emit('response', {'data': response_data})


@sockets.on('disconnect', namespace='/api')
def test_disconnect():
    print 'Client disconnected'
    data_generator.stop_generation()


def run_with_heartbeat_settings():
    sockets.run(app, heartbeat_interval=20000, heartbeat_timeout=20000)


if __name__ == '__main__':
    sockets.run(app)
