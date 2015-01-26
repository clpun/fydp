from flask import Flask, render_template
from flask.ext.socketio import SocketIO, emit
import socket
from py.src import mindcraft

app = Flask(__name__)
sockets = SocketIO(app)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/webSoc', methods=['GET'])
def web_soc_fun():
    return render_template('websocket.html')

@sockets.on('request', namespace='/api')
def get_power(message):
	for i in mindcraft.main():
		#print str(i)
		emit('response', {'data': i})

# @sockets.on('request', namespace='/api')
# def get_userid(message):
# 	print 'getting userid from server'
# 	print str(mindcraft.get_userid())
# 	emit('response',{'data': {'userid':mindcraft.get_userid()}})
# 	return

@sockets.on('disconnect', namespace='/api')
def test_disconnect():
    print('Client disconnected')

def __main__():
	sockets.run(app,heartbeat_interval=20000,heartbeat_timeout=20000)

if __name__ == '__main__':
	sockets.run(app)
