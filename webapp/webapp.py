from flask import Flask, render_template
from flask import jsonify
from flask.ext.socketio import SocketIO, emit
from py.src import mindcraft
from py.src.test_data_generator import TestDataGenerator
import thread
from threading import Event

app = Flask(__name__)
sockets = SocketIO(app)

test_data_generator = TestDataGenerator()

stop_streaming_event = Event()
data_emitter_thread = None

test_mode = False

def run_server():
    sockets.run(app)


@sockets.on('connect', namespace='/api')
def connected():
    global data_emitter_thread
    print 'Client connected'
    if data_emitter_thread is None:
        print 'Starting headset_data_handler'
        data_emitted_thread = thread.start_new_thread(headset_data_handler, ())


def headset_data_handler():
    global test_mode
    while not stop_streaming_event.isSet():
        if test_mode:
            for data_point in test_data_generator.generate_data():
                if not test_mode:
                    break
                sockets.emit('response', {'data': data_point}, namespace='/api')
        else:
            for data_point in mindcraft.main():
                if test_mode:
                    break
                sockets.emit('response', {'data': data_point}, namespace='/api')


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/webSoc', methods=['GET'])
def web_soc_fun():
    return render_template('websocket.html')


# TODO: combine these two?
@app.route('/enable_test_mode')
def enable_test_mode():
    global test_mode
    test_mode = True
    return jsonify(test_mode=True)

@app.route('/disable_test_mode')
def disable_test_mode():
    global test_mode
    test_mode = False
    return jsonify(test_mode=False)


@sockets.on('request', namespace='/api')
def get_power(message):
    for i in mindcraft.main():
        emit('response', {'data': i})


@sockets.on('request_test_data', namespace='/api')
def get_power_test_data(message):
    for response_data in test_data_generator.generate_data():
        print 'Sending response test data: %s' % response_data
        emit('response', {'data': response_data})


@sockets.on('disconnect', namespace='/api')
def disconnected():
    print 'Client disconnected'
    # TODO: stop headset? (by setting stop_streaming_event


def run_with_heartbeat_settings():
    sockets.run(app, heartbeat_interval=20000, heartbeat_timeout=20000)


if __name__ == '__main__':
    run_server()
