from flask import Flask, render_template
from flask.ext.socketio import SocketIO, emit
import py.src.developerAPI as devapi

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
	# print "Server side: request granted"
	# print 'verify = ' + str(devapi.get_userid())
	emit('response',{'data': devapi.get_all_power()})
	return
# def test_message(message):
#     print 'received: %s' % message
#     for i in range(1, 10):
#         emit('response', {'data': [21, 22, 53, 78, 45]})
#     return
# def get_power(power_range,channel):
# 	print power_range + ' : ' + channel
# 	if power_range == 'Delta':
# 		devapi.get_delta_sum_mag(channel)
# 	elif power_range == 'Theta':
# 		devapi.get_theta_sum_mag(channel)
# 	elif power_range == 'Alpha':
# 		devapi.get_alpha_sum_mag(channel)
# 	elif power_range == 'Beta':
# 		devapi.get_beta_sum_mag(channel)
# 	elif power_range == 'Gamma':
# 		devapi.get_gamma_sum_mag(channel)
# 	return

@sockets.on('request_userid', namespace='/api')
def get_userid(message):
	emit('response',{'data': devapi.get_userid()})
	return

@sockets.on('disconnect', namespace='/api')
def test_disconnect():
    print('Client disconnected')

def __main__():
	sockets.run(app)

def write_userid(userid):
	print 'user id = ' + userid
	devapi.write_userid(userid)

def write_delta_sum_mag(channel,power) :
	devapi.write_delta_sum_mag(channel,power)

def write_theta_sum_mag(channel,power) :
	devapi.write_theta_sum_mag(channel,power)

def write_alpha_sum_mag(channel,power) :
	devapi.write_alpha_sum_mag(channel,power)

def write_beta_sum_mag(channel,power) :
	devapi.write_beta_sum_mag(channel,power)

def write_gamma_sum_mag(channel,power) :
	devapi.write_gamma_sum_mag(channel,power)

def format_data_to_emit() :
	devapi.format_data_to_emit()

if __name__ == '__main__':
    sockets.run(app)
