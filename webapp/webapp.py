from flask import Flask, render_template
from flask import jsonify
from flask import request, g
from flask.ext.socketio import SocketIO, emit
from py.src import mindcraft
from py.src.test_data_generator import TestDataGenerator
import thread
from threading import Event
import time

app = Flask(__name__)
sockets = SocketIO(app)

test_data_generator = TestDataGenerator()

channels = ['F3','FC5','AF3','F7','T7','P7','O1','O2','P8','T8','F8','AF4','FC6','F4']
bands = ['gamma','beta','alpha','theta','delta']

samplingPeriod = 0.25
duration = 30
recordingDuration = 0
stop_streaming_event = Event()
start_recording_event = Event()
data_emitter_thread = None
csvDataBuffer = {}
csvDataIndex = 0

test_mode = False

def run_server():
    sockets.run(app)


@sockets.on('connect', namespace='/api')
def connected():
    print 'Client connected'
    start_streaming()


def headset_data_handler():
    global test_mode
    global recordingDuration
    global csvDataBuffer
    global csvDataIndex

    while not stop_streaming_event.isSet():
        if test_mode:
            for data_point in test_data_generator.generate_data():
                if not test_mode or stop_streaming_event.isSet():
                    break
                if start_recording_event.isSet():
                	print "recording... = " + str(recordingDuration*100/duration) + "%"
                	if recordingDuration >= duration:
                		stop_recording()
                	# data_point format: {"delta":{{"F3":123,"F4":123}},"theta":{},"alpha":{},"beta":{},"gamma":{}}
                	csvDataBuffer[csvDataIndex] = data_point
                	csvDataIndex += 1
                	recordingDuration += 1
                sockets.emit('response', {'data': data_point}, namespace='/api')
        else:
            for data_point in mindcraft.main():
                if test_mode or stop_streaming_event.isSet():
                    break
                if start_recording_event.isSet():
                	print "recording... = " + str(recordingDuration*100/duration) + "%"
                	if recordingDuration >= duration:
                		stop_recording()
                	# data_point format: {"delta":{{"F3":123,"F4":123}},"theta":{},"alpha":{},"beta":{},"gamma":{}}
                	csvDataBuffer[csvDataIndex] = data_point
                	csvDataIndex += 1
                	recordingDuration += 1
                sockets.emit('response', {'data': data_point}, namespace='/api')

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/webSoc', methods=['GET'])
def web_soc_fun():
    return render_template('websocket.html')

@app.route('/verify_user')
def verify_user():
	print 'Verify User'
	mindcraft.verify_user()
	return jsonify(verifiedUser=True)

@app.route('/start_recording/<int:period>')
def start_recording(period):
	global duration
	global start_recording_event
	global stop_streaming_event
	global data_emitter_thread
	duration = period/samplingPeriod
	print "start_recording : " + str(duration) + " samples"
	if data_emitter_thread is None:
		start_recording_event.set()
		stop_streaming_event.clear()
		print 'Starting headset_data_handler'
		data_emitter_thread = thread.start_new_thread(headset_data_handler, ())
	return jsonify(recording=True)

@app.route('/stop_recording')
def client_request_stop_recording():
	stop_recording()
	return jsonify(recording=False)

def stop_recording():
	print "stop recording"
	global start_recording_event
	global stop_streaming_event
	global data_emitter_thread
	global recordingDuration
	start_recording_event.clear()
	stop_streaming_event.set()
	data_emitter_thread = None
	recordingDuration = 0
	sockets.emit('notification', {'data': 'recording_done'}, namespace='/api')

@app.route('/write_to_csv')
def write_to_csv():
	global csvDataBuffer

	csv_data = "time,"
	for band in bands:
		for channel in channels:
			csv_data += channel + "(" + band + "),"
	csv_data += "\n"
	for index in csvDataBuffer.keys():
		csv_data += str(int(index)*samplingPeriod) + ","
		for band in bands:
			for channel in channels:
				csv_data += str(csvDataBuffer[index][band][channel]) + ","
		csv_data += "\n"
	
	fo = open("test_data/time_frequency_plot_" + time.strftime("%d%b%Y_%H%M%S",time.localtime()) + ".csv","wb")
	fo.write(csv_data)
	fo.close()
	clear_recording_buffer()
	return jsonify(writing_succeeded=True)

@app.route('/clear_recording_buffer')
def clear_recording_buffer():
	global csvDataBuffer
	global csvDataIndex
	global recordingDuration
	recordingDuration = 0
	csvDataIndex = 0
	csvDataBuffer = {}
	print "Cleared recording buffer"

# TODO: combine these two?
@app.route('/start_streaming')
def start_streaming():
    global stop_streaming_event
    global data_emitter_thread
    if data_emitter_thread is None:
        stop_streaming_event.clear()
        print 'Starting headset_data_handler'
        data_emitter_thread = thread.start_new_thread(headset_data_handler, ())
    return jsonify(streaming=True)

@app.route('/stop_streaming')
def stop_streaming():
    global stop_streaming_event
    global data_emitter_thread
    stop_streaming_event.set()
    data_emitter_thread = None
    return jsonify(streaming=False)


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
