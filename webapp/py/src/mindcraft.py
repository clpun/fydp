import sys
#sys.path.append("..")
from ..lib import emotiv
import gevent
import numpy as np
import math
import csv
import time
import os

import select
import fft
import signal_preprocessing as sp
import check_signal_quality

samplingFreq = 128.0
fftSamplingNum = 26.0
oneFftPeriod = fftSamplingNum/samplingFreq

server_testing_mode = 0
if server_testing_mode:
    import developerAPI as devapi
    import random
    from websocket import create_connection
    import socket

headset = emotiv.Emotiv()
start_time = time.time()

class UserPreference:
    user_name = "User"
    env_offset_avg_var = {}
    def write_env_offset_avg_var(self,name,var):
        self.env_offset_avg_var.update({name: var})

    def read_env_offset_avg_var(self,name):
        return self.env_offset_avg_var[name]


user_preference = UserPreference()

# Variables for the sum magnitude of the 5 frequency bands. 

delta_sum_mag = {}
theta_sum_mag = {}
alpha_sum_mag = {}
beta_sum_mag = {}
gamma_sum_mag = {}

band_types = ['delta', 'theta', 'alpha', 'beta', 'gamma']
sensor_names = ['F3', 'FC5', 'AF3', 'F7', 'T7', 'P7', 'O1', 'O2', 'P8', 'T8', 'F8', 'AF4', 'FC6', 'F4']

gyroX = 0.0
gyroY = 0.0
battery = 0.0
contact_quality = {}

# Variables to calculate first derivative
_gyroX = 0.0
_gyroY = 0.0

# Transition Frequencies Variables
cal_tf_duration_in_second = 30.0
cal_tf_duration = math.ceil(cal_tf_duration_in_second/oneFftPeriod)
tf_delta_theta = {}
tf_theta_alpha = {}
tf_alpha_beta = {}
tf_beta_gamma = {}
for sensor in sensor_names:
    tf_delta_theta[sensor] = 2
    tf_theta_alpha[sensor] = 4
    tf_alpha_beta[sensor] = 9
    tf_beta_gamma[sensor] = 31

# Variables for Pattern Analysis
import mindcraft_classifier as mclassifier
from enum import Enum
class classifier_type(Enum):
    temporal_working_memory = 1
fft_lut_t = {}      # Look Up Table
fft_lut_circbuffersize = 8
fft_lut_circbufferindex = fft_lut_circbuffersize - 1
for sensor in sensor_names:
    fft_lut_t[sensor] = np.empty(63,dtype='<i4')
    for ii in range(0,64):
        fft_lut_t[sensor][ii] = np.empty(fft_lut_circbuffersize,dtype='<f8')

# Initialize sensor pointer
F3 = {}
FC5 = {}
AF3 = {}
F7 = {}
T7 = {}
P7 = {}
O1 = {}
O2 = {}
P8 = {}
T8 = {}
F8 = {}
AF4 = {}
FC6 = {}
F4 = {}

# Initialize sensor buffers
F3Buffer = []
FC5Buffer = []
AF3Buffer = []
F7Buffer = []
T7Buffer = []
P7Buffer = []
O1Buffer = []
O2Buffer = []
P8Buffer = []
T8Buffer = []
F8Buffer = []
AF4Buffer = []
FC6Buffer = []
F4Buffer = []

def verify_user():
    global user_preference
    global headset
    global f3_mean
    global fc5_mean
    global af3_mean
    global f7_mean
    global t7_mean
    global p7_mean
    global o1_mean
    global o2_mean
    global p8_mean
    global t8_mean
    global f8_mean
    global af4_mean
    global fc6_mean
    global f4_mean

    user_verify = False
    while not user_verify:
        user_name = raw_input("User id: ")
        if user_name.isalnum():
            user_preference.user_name = user_name
            try:
                if os.path.exists(user_name + '.txt'):
                    pref_file = open(user_name + '.txt','r+')
                else:
                    pref_file = open(user_name + '.txt','w+')
                    print "Welcome new user : " + user_name
                line = pref_file.readline()
                while line != '':
                    elements = line.split(':')
                    if len(elements) == 2:
                        if elements[0] == 'f3_mean':
                            user_preference.write_env_offset_avg_var('f3_mean',float(elements[1]))
                        elif elements[0] == 'fc5_mean':
                            user_preference.write_env_offset_avg_var('fc5_mean',float(elements[1]))
                        elif elements[0] == 'af3_mean':
                            user_preference.write_env_offset_avg_var('af3_mean',float(elements[1]))
                        elif elements[0] == 'f7_mean':
                            user_preference.write_env_offset_avg_var('f7_mean',float(elements[1]))
                        elif elements[0] == 't7_mean':
                            user_preference.write_env_offset_avg_var('t7_mean',float(elements[1]))
                        elif elements[0] == 'p7_mean':
                            user_preference.write_env_offset_avg_var('p7_mean',float(elements[1]))
                        elif elements[0] == 'o1_mean':
                            user_preference.write_env_offset_avg_var('o1_mean',float(elements[1]))
                        elif elements[0] == 'o2_mean':
                            user_preference.write_env_offset_avg_var('o2_mean',float(elements[1]))
                        elif elements[0] == 'p8_mean':
                            user_preference.write_env_offset_avg_var('p8_mean',float(elements[1]))
                        elif elements[0] == 't8_mean':
                            user_preference.write_env_offset_avg_var('t8_mean',float(elements[1]))
                        elif elements[0] == 'f8_mean':
                            user_preference.write_env_offset_avg_var('f8_mean',float(elements[1]))
                        elif elements[0] == 'af4_mean':
                            user_preference.write_env_offset_avg_var('af4_mean',float(elements[1]))
                        elif elements[0] == 'fc6_mean':
                            user_preference.write_env_offset_avg_var('fc6_mean',float(elements[1]))
                        elif elements[0] == 'f4_mean':
                            user_preference.write_env_offset_avg_var('f4_mean',float(elements[1]))
                        else:
                            pass
                    line = pref_file.readline()
                pref_file.close()
                if len(user_preference.env_offset_avg_var) == 0:
                    find_mean()
                    pref_file = open(user_name + '.txt','w')
                    param = []
                    for keys in user_preference.env_offset_avg_var:
                        param.append(keys + ':' + str(user_preference.env_offset_avg_var[keys])+'\n')
                    pref_file.writelines(param)
                    pref_file.close()
                    user_verify = True
                else:
                    prompt_calculate_average = raw_input("\nY: Use Previous Signal Average, N: Recalculate Signal Average\n")
                    while not (prompt_calculate_average == 'Y' or prompt_calculate_average == 'N'):
                        prompt_calculate_average = raw_input("\nY: Use Previous Signal Average, N: Recalculate Signal Average\n")
                    if prompt_calculate_average == 'Y':
                        f3_mean = user_preference.read_env_offset_avg_var('f3_mean')
                        fc5_mean = user_preference.read_env_offset_avg_var('fc5_mean')
                        af3_mean = user_preference.read_env_offset_avg_var('af3_mean')
                        f7_mean = user_preference.read_env_offset_avg_var('f7_mean')
                        t7_mean = user_preference.read_env_offset_avg_var('t7_mean')
                        p7_mean = user_preference.read_env_offset_avg_var('p7_mean')
                        o1_mean = user_preference.read_env_offset_avg_var('o1_mean')
                        o2_mean = user_preference.read_env_offset_avg_var('o2_mean')
                        p8_mean = user_preference.read_env_offset_avg_var('p8_mean')
                        t8_mean = user_preference.read_env_offset_avg_var('t8_mean')
                        f8_mean = user_preference.read_env_offset_avg_var('f8_mean')
                        af4_mean = user_preference.read_env_offset_avg_var('af4_mean')
                        fc6_mean = user_preference.read_env_offset_avg_var('fc6_mean')
                        f4_mean = user_preference.read_env_offset_avg_var('f4_mean')
                        user_verify = True
                    elif prompt_calculate_average == 'N':
                        find_mean()
                        pref_file = open(user_name + '.txt','w')
                        param = []
                        for keys in user_preference.env_offset_avg_var:
                            param.append(keys + ':' + str(user_preference.env_offset_avg_var[keys])+'\n')
                        pref_file.writelines(param)
                        pref_file.close()
                        user_verify = True

                if not user_verify:
                    print "Something is wrong with the environment offset average variables. Please use another user id."
                else:
                    print 'check signal quality'
                    #check_signal_quality.run(headset)

            except IOError:
                print "IO Error"
            except RuntimeError:
                user_verify = False
                print "User id is corrupted. Please use another user id."
                pref_file.close()
        else:
            print "Invalid user id. Please use an alphanumeric id."

def load_dvs():
    mclassifier.load_mean_decision_values(classifier_type.temporal_working_memory,'check_dv_median_all_DV_accepted.csv')

def clear_buffers():
    del F3Buffer[:]
    del FC5Buffer[:]
    del AF3Buffer[:]
    del F7Buffer[:]
    del T7Buffer[:]
    del P7Buffer[:]
    del O1Buffer[:]
    del O2Buffer[:]
    del P8Buffer[:]
    del T8Buffer[:]
    del F8Buffer[:]
    del AF4Buffer[:]
    del FC6Buffer[:]
    del F4Buffer[:]

def find_mean():
    global user_preference
    headset = emotiv.Emotiv()
    gevent.spawn(headset.setup)
    gevent.sleep(1)
    counter = 0

    raw_input("Need to Calculate signal average. Do NOT wear the headset. Please press enter to continue...")
    print("Calculating signal average. Please wait...")

    headset.packets.queue.clear()
    while counter < 1000:
        print "..." + str((counter+1)/10) + "%"
        # Retrieve emotiv packet
        #headset = emotiv.Emotiv()
        packet = headset.dequeue()

        # Get sensor data
        F3 = packet.sensors['F3']['value']
        FC5 = packet.sensors['FC5']['value']
        AF3 = packet.sensors['AF3']['value']
        F7 = packet.sensors['F7']['value']
        T7 = packet.sensors['T7']['value']
        P7 = packet.sensors['P7']['value']
        O1 = packet.sensors['O1']['value']
        O2 = packet.sensors['O2']['value']
        P8 = packet.sensors['P8']['value']
        T8 = packet.sensors['T8']['value']
        F8 = packet.sensors['F8']['value']
        AF4 = packet.sensors['AF4']['value']
        FC6 = packet.sensors['FC6']['value']
        F4 = packet.sensors['F4']['value']

        # Build buffers for FFT
        F3Buffer.append(F3)
        FC5Buffer.append(FC5)
        AF3Buffer.append(AF3)
        F7Buffer.append(F7)
        T7Buffer.append(T7)
        P7Buffer.append(P7)
        O1Buffer.append(O1)
        O2Buffer.append(O2)
        P8Buffer.append(P8)
        T8Buffer.append(T8)
        F8Buffer.append(F8)
        AF4Buffer.append(AF4)
        FC6Buffer.append(FC6)
        F4Buffer.append(F4)

        counter = counter + 1

    global f3_mean
    f3_mean = np.mean(F3Buffer)
    user_preference.write_env_offset_avg_var('f3_mean',f3_mean)
    global fc5_mean
    fc5_mean = np.mean(FC5Buffer)
    user_preference.write_env_offset_avg_var('fc5_mean',fc5_mean)
    global af3_mean
    af3_mean = np.mean(AF3Buffer)
    user_preference.write_env_offset_avg_var('af3_mean',af3_mean)
    global f7_mean
    f7_mean = np.mean(F7Buffer)
    user_preference.write_env_offset_avg_var('f7_mean',f7_mean)
    global t7_mean
    t7_mean = np.mean(T7Buffer)
    user_preference.write_env_offset_avg_var('t7_mean',t7_mean)
    global p7_mean
    p7_mean = np.mean(P7Buffer)
    user_preference.write_env_offset_avg_var('p7_mean',p7_mean)
    global o1_mean
    o1_mean = np.mean(O1Buffer)
    user_preference.write_env_offset_avg_var('o1_mean',o1_mean)
    global o2_mean
    o2_mean = np.mean(O2Buffer)
    user_preference.write_env_offset_avg_var('o2_mean',o2_mean)
    global p8_mean
    p8_mean = np.mean(P8Buffer)
    user_preference.write_env_offset_avg_var('p8_mean',p8_mean)
    global t8_mean
    t8_mean = np.mean(T8Buffer)
    user_preference.write_env_offset_avg_var('t8_mean',t8_mean)
    global f8_mean
    f8_mean = np.mean(F8Buffer)
    user_preference.write_env_offset_avg_var('f8_mean',f8_mean)
    global af4_mean
    af4_mean = np.mean(AF4Buffer)
    user_preference.write_env_offset_avg_var('af4_mean',af4_mean)
    global fc6_mean
    fc6_mean = np.mean(FC6Buffer)
    user_preference.write_env_offset_avg_var('fc6_mean',fc6_mean)
    global f4_mean
    f4_mean = np.mean(F4Buffer)
    user_preference.write_env_offset_avg_var('f4_mean',f4_mean)

    clear_buffers()

def analyze_pattern():
    global _gyroX
    global _gyroY
    global fft_lut_t

    tmw_control = mclassifier.twm_mean_classifier(fft_lut_t,fft_lut_circbufferindex)
    if tmw_control:
        print "tmw control!"
    # print "Battery = " + str(battery)
    # if float(battery) < 5:
    #     print "Need to recharge battery: " + str(battery)
    #print "Change of gyroX = " + str(_gyroX - gyroX)
    #print "Change of gyroY = " + str(_gyroY - gyroY)
    _gyroX = gyroX
    _gyroY = gyroY
    #print "--------------------"

def main():
    global headset
    global fft_lut_t

    headset = emotiv.Emotiv()
    gevent.spawn(headset.setup)
    gevent.sleep(1)

    try:
        sample_counter = 0
        headset.packets.queue.clear()
        while True:
            dequeue_headset()
            sample_counter = sample_counter + 1

            # Do FFT for each sensor after collecting 32 samples
            if sample_counter > fftSamplingNum:
                # print "pass = " + str(len(fft_lut_t[sensor])-1)
                # Remove high frequency noise and dc offset
                # Apply DFT to extract frequency components
                f3_fft = fft.compute_fft(sp.preprocess(F3Buffer, f3_mean))
                fc5_fft = fft.compute_fft(sp.preprocess(FC5Buffer, fc5_mean))
                af3_fft = fft.compute_fft(sp.preprocess(AF3Buffer, af3_mean))
                f7_fft = fft.compute_fft(sp.preprocess(F7Buffer, f7_mean))
                t7_fft = fft.compute_fft(sp.preprocess(T7Buffer, t7_mean))
                p7_fft = fft.compute_fft(sp.preprocess(P7Buffer, p7_mean))
                o1_fft = fft.compute_fft(sp.preprocess(O1Buffer, o1_mean))
                o2_fft = fft.compute_fft(sp.preprocess(O2Buffer, o2_mean))
                p8_fft = fft.compute_fft(sp.preprocess(P8Buffer, p8_mean))
                t8_fft = fft.compute_fft(sp.preprocess(T8Buffer, t8_mean))
                f8_fft = fft.compute_fft(sp.preprocess(F8Buffer, f8_mean))
                af4_fft = fft.compute_fft(sp.preprocess(AF4Buffer, af4_mean))
                fc6_fft = fft.compute_fft(sp.preprocess(FC6Buffer, fc6_mean))
                f4_fft = fft.compute_fft(sp.preprocess(F4Buffer, f4_mean))

                for sensor in sensor_names:
                    if sensor == 'F3':
                        fft_comp = f3_fft
                    elif sensor == 'FC5':
                        fft_comp = fc5_fft
                    elif sensor == 'AF3':
                        fft_comp = af3_fft
                    elif sensor == 'F7':
                        fft_comp = f7_fft
                    elif sensor == 'T7':
                        fft_comp = t7_fft
                    elif sensor == 'P7':
                        fft_comp = p7_fft
                    elif sensor == 'O1':
                        fft_comp = o1_fft
                    elif sensor == 'O2':
                        fft_comp = o2_fft
                    elif sensor == 'P8':
                        fft_comp = p8_fft
                    elif sensor == 'T8':
                        fft_comp = t8_fft
                    elif sensor == 'F8':
                        fft_comp = f8_fft
                    elif sensor == 'AF4':
                        fft_comp = af4_fft
                    elif sensor == 'FC6':
                        fft_comp = fc6_fft
                    elif sensor == 'F4':
                        fft_comp = f4_fft
                    for ii in range(0,len(fft_comp)-1):
                        update_fft_lut_circbufferindex()
                        fft_lut_t[sensor][ii][fft_lut_circbufferindex] = fft_comp[ii]

                analyze_pattern()
                # Clear buffers
                clear_buffers()
                sample_counter = 0

            gevent.sleep(0)

    except KeyboardInterrupt:
        headset.close()
    finally:
        headset.close()

def calculate_tf(cal_tf_data):
    tf_matrix = {}
    iaf_matrix = {}
    for sensor in sensor_names:
        #Find IAF and transition freq (tf) from 7Hz to 13Hz
        iaf = 0
        # expectation and expectationSquared is used to calculate the variance between 4Hz to 13Hz across all samples
        expectation = {}
        expectationSquared = {}
        for jj in range(4,13):
            expectation[str(jj)] = 0.0
            expectationSquared[str(jj)] = 0.0
        #Find IAF
        for ii in range(0,len(cal_tf_data)-1):
            slice_iaf = cal_tf_data[ii][sensor][7]
            min_iaf = 7
            for jj in range(8,13):
                if data[ii][sensor][jj] >= slice_iaf:
                    min_iaf = jj
                    slice_iaf = cal_tf_data[ii][sensor][jj]
            iaf += int(min_iaf)
        iaf_matrix[sensor] = int(iaf/float(len(cal_tf_data)))
        #Find tf
        for ii in range(0,len(cal_tf_data)-1):
            for jj in range(4,iaf_matrix[sensor]-1):
                expectation[str(jj)] += cal_tf_data[ii][sensor][jj]
                expectationSquared[str(jj)] += (cal_tf_data[ii][sensor][jj])**2

        for jj in range(4,iaf_matrix[sensor]-1):
            expectation[str(jj)] /= float(len(cal_tf_data))
            expectationSquared[str(jj)] /= float(len(cal_tf_data))
        tf = expectationSquared['4'] - (expectation['4'])**2
        tf_matrix[sensor] = 4
        for jj in range(5,iaf_matrix[sensor]-1):
            variance = expectationSquared[str(jj)] - (expectation[str(jj)])**2
            if variance <= tf:
                tf = variance
                tf_matrix[sensor] = jj

    for sensor in sensor_names:
        print "For " + sensor + ":"
        print "----------iaf = " + str(iaf_matrix[sensor])
        print "----------tf_dt = " + str(tf_matrix[sensor] - 2)
        print "----------tf_ta = " + str(tf_matrix[sensor])
        print "----------tf_ab = " + str(5.0 + tf_matrix[sensor])
        tf_delta_theta[sensor] = int(tf_matrix[sensor] - 2)
        tf_theta_alpha[sensor] = int(tf_matrix[sensor])
        tf_alpha_beta[sensor] = int(5.0 + tf_matrix[sensor])
        tf_beta_gamma[sensor] = 31

def calculate_transition_frequencies():
    global headset
    headset = emotiv.Emotiv()
    gevent.spawn(headset.setup)
    gevent.sleep(1)
    cal_tf_data = {}
    index = 0
    try:
        sample_counter = 0
        while index <= cal_tf_duration:
            dequeue_headset()
            sample_counter = sample_counter + 1
            # Do FFT for each sensor after collecting 32 samples
            if sample_counter > fftSamplingNum:
                # Remove high frequency noise and dc offset
                # Apply DFT to extract frequency components
                f3_fft = fft.compute_fft(sp.preprocess(F3Buffer, f3_mean))
                fc5_fft = fft.compute_fft(sp.preprocess(FC5Buffer, fc5_mean))
                af3_fft = fft.compute_fft(sp.preprocess(AF3Buffer, af3_mean))
                f7_fft = fft.compute_fft(sp.preprocess(F7Buffer, f7_mean))
                t7_fft = fft.compute_fft(sp.preprocess(T7Buffer, t7_mean))
                p7_fft = fft.compute_fft(sp.preprocess(P7Buffer, p7_mean))
                o1_fft = fft.compute_fft(sp.preprocess(O1Buffer, o1_mean))
                o2_fft = fft.compute_fft(sp.preprocess(O2Buffer, o2_mean))
                p8_fft = fft.compute_fft(sp.preprocess(P8Buffer, p8_mean))
                t8_fft = fft.compute_fft(sp.preprocess(T8Buffer, t8_mean))
                f8_fft = fft.compute_fft(sp.preprocess(F8Buffer, f8_mean))
                af4_fft = fft.compute_fft(sp.preprocess(AF4Buffer, af4_mean))
                fc6_fft = fft.compute_fft(sp.preprocess(FC6Buffer, fc6_mean))
                f4_fft = fft.compute_fft(sp.preprocess(F4Buffer, f4_mean))

                cal_tf_data[index] = {}
                for sensor in sensor_names:
                    if sensor == 'F3':
                        fft_comp = f3_fft
                    elif sensor == 'FC5':
                        fft_comp = fc5_fft
                    elif sensor == 'AF3':
                        fft_comp = af3_fft
                    elif sensor == 'F7':
                        fft_comp = f7_fft
                    elif sensor == 'T7':
                        fft_comp = t7_fft
                    elif sensor == 'P7':
                        fft_comp = p7_fft
                    elif sensor == 'O1':
                        fft_comp = o1_fft
                    elif sensor == 'O2':
                        fft_comp = o2_fft
                    elif sensor == 'P8':
                        fft_comp = p8_fft
                    elif sensor == 'T8':
                        fft_comp = t8_fft
                    elif sensor == 'F8':
                        fft_comp = f8_fft
                    elif sensor == 'AF4':
                        fft_comp = af4_fft
                    elif sensor == 'FC6':
                        fft_comp = fc6_fft
                    elif sensor == 'F4':
                        fft_comp = f4_fft

                    cal_tf_data[index][sensor] = fft_comp

                # Clear buffers
                clear_buffers()
                sample_counter = 0
                index += 1

            gevent.sleep(0)
        calculate_tf(cal_tf_data)
    except KeyboardInterrupt:
        headset.close()
    finally:
        headset.close()

def update_fft_lut_circbufferindex():
    global fft_lut_circbufferindex
    fft_lut_circbufferindex += 1
    if fft_lut_circbufferindex == fft_lut_circbuffersize:
        fft_lut_circbufferindex = 0

def get_individual_frequency_power():
    global headset
    headset = emotiv.Emotiv()
    gevent.spawn(headset.setup)
    gevent.sleep(1)
    try:
        sample_counter = 0
        headset.packets.queue.clear()
        while True:
            dequeue_headset()
            sample_counter = sample_counter + 1
            # Do FFT for each sensor after collecting 32 samples
            if sample_counter > fftSamplingNum:
                # Remove high frequency noise and dc offset
                # Apply DFT to extract frequency components
                f3_fft = fft.compute_fft(sp.preprocess(F3Buffer, f3_mean))
                fc5_fft = fft.compute_fft(sp.preprocess(FC5Buffer, fc5_mean))
                af3_fft = fft.compute_fft(sp.preprocess(AF3Buffer, af3_mean))
                f7_fft = fft.compute_fft(sp.preprocess(F7Buffer, f7_mean))
                t7_fft = fft.compute_fft(sp.preprocess(T7Buffer, t7_mean))
                p7_fft = fft.compute_fft(sp.preprocess(P7Buffer, p7_mean))
                o1_fft = fft.compute_fft(sp.preprocess(O1Buffer, o1_mean))
                o2_fft = fft.compute_fft(sp.preprocess(O2Buffer, o2_mean))
                p8_fft = fft.compute_fft(sp.preprocess(P8Buffer, p8_mean))
                t8_fft = fft.compute_fft(sp.preprocess(T8Buffer, t8_mean))
                f8_fft = fft.compute_fft(sp.preprocess(F8Buffer, f8_mean))
                af4_fft = fft.compute_fft(sp.preprocess(AF4Buffer, af4_mean))
                fc6_fft = fft.compute_fft(sp.preprocess(FC6Buffer, fc6_mean))
                f4_fft = fft.compute_fft(sp.preprocess(F4Buffer, f4_mean))

                # Calculate the magnitude sum of the 5 frequency bands.
                # Delta = 1-3 Hz [0:tf_delta_theta]
                # Theta = 4-7 Hz [tf_delta_theta+1:tf_theta_alpha]
                # Alpha = 8-15 Hz [tf_theta_alpha+1:tf_alpha_beta]
                # Beta = 16-31 Hz [tf_alpha_beta+1:tf_beta_gamma]
                # Gamma = 32-64 Hz [32:-1]

                # Determine if a freq band of a channel has a steady increase in magnitude over 3 ffts
                power_dict = {}
                power_dict['indiv_component'] = {}
                power_dict['quality'] = {}
                for sensor in sensor_names:
                    power_dict['indiv_component'][sensor] = {}
                    if sensor == 'F3':
                        fft_comp = f3_fft
                    elif sensor == 'FC5':
                        fft_comp = fc5_fft
                    elif sensor == 'AF3':
                        fft_comp = af3_fft
                    elif sensor == 'F7':
                        fft_comp = f7_fft
                    elif sensor == 'T7':
                        fft_comp = t7_fft
                    elif sensor == 'P7':
                        fft_comp = p7_fft
                    elif sensor == 'O1':
                        fft_comp = o1_fft
                    elif sensor == 'O2':
                        fft_comp = o2_fft
                    elif sensor == 'P8':
                        fft_comp = p8_fft
                    elif sensor == 'T8':
                        fft_comp = t8_fft
                    elif sensor == 'F8':
                        fft_comp = f8_fft
                    elif sensor == 'AF4':
                        fft_comp = af4_fft
                    elif sensor == 'FC6':
                        fft_comp = fc6_fft
                    elif sensor == 'F4':
                        fft_comp = f4_fft

                    delta_sum_mag[sensor] = sum(fft_comp[0:tf_delta_theta[sensor]])
                    theta_sum_mag[sensor] = sum(fft_comp[tf_delta_theta[sensor]+1:tf_theta_alpha[sensor]])
                    alpha_sum_mag[sensor] = sum(fft_comp[tf_theta_alpha[sensor]+1:tf_alpha_beta[sensor]])
                    beta_sum_mag[sensor] = sum(fft_comp[tf_alpha_beta[sensor]+1:tf_beta_gamma[sensor]])
                    gamma_sum_mag[sensor] = sum(fft_comp[tf_beta_gamma[sensor]+1:])
                    for ii in range(0,len(fft_comp)-1):
                        power_dict['indiv_component'][sensor][str(ii)] = fft_comp[ii]

                for band in band_types:
                    power_dict[band] = {}
                    for sensor in sensor_names:
                        if band == "delta" :
                            power_dict[band][sensor] = delta_sum_mag[sensor]
                        elif band == "theta":
                            power_dict[band][sensor] = theta_sum_mag[sensor]
                        elif band == "alpha":
                            power_dict[band][sensor] = alpha_sum_mag[sensor]
                        elif band == "beta":
                            power_dict[band][sensor] = beta_sum_mag[sensor]
                        elif band == "gamma":
                            power_dict[band][sensor] = gamma_sum_mag[sensor]
                
                power_dict['quality']['F3'] = F3['quality']
                power_dict['quality']['FC5'] = FC5['quality']
                power_dict['quality']['AF3'] = AF3['quality']
                power_dict['quality']['F7'] = F7['quality']
                power_dict['quality']['T7'] = T7['quality']
                power_dict['quality']['P7'] = P7['quality']
                power_dict['quality']['O1'] = O1['quality']
                power_dict['quality']['O2'] = O2['quality']
                power_dict['quality']['P8'] = P8['quality']
                power_dict['quality']['T8'] = T8['quality']
                power_dict['quality']['F8'] = F8['quality']
                power_dict['quality']['AF4'] = AF4['quality']
                power_dict['quality']['FC6'] = FC6['quality']
                power_dict['quality']['F4'] = F4['quality']

                #print "printing time for every emit = "+str(time.time())
                yield power_dict

                # Clear buffers
                clear_buffers()
                sample_counter = 0

            gevent.sleep(0)

    except KeyboardInterrupt:
        headset.close()
    finally:
        headset.close()

def dequeue_headset():
    global headset
    global gyroX
    global gyroY
    global battery
    global F3
    global FC5
    global AF3
    global F7
    global T7
    global P7
    global O1
    global O2
    global P8
    global T8
    global F8
    global AF4
    global FC6
    global F4
    # Retrieve emotiv packet
    packet = headset.dequeue()

    battery = packet.battery
    gyroX = packet.sensors['X']['value']
    gyroY = packet.sensors['Y']['value']

    F3 = packet.sensors['F3']
    FC5 = packet.sensors['FC5']
    AF3 = packet.sensors['AF3']
    F7 = packet.sensors['F7']
    T7 = packet.sensors['T7']
    P7 = packet.sensors['P7']
    O1 = packet.sensors['O1']
    O2 = packet.sensors['O2']
    P8 = packet.sensors['P8']
    T8 = packet.sensors['T8']
    F8 = packet.sensors['F8']
    AF4 = packet.sensors['AF4']
    FC6 = packet.sensors['FC6']
    F4 = packet.sensors['F4']

    # Build buffers for FFT
    F3Buffer.append(F3['value'])
    FC5Buffer.append(FC5['value'])
    AF3Buffer.append(AF3['value'])
    F7Buffer.append(F7['value'])
    T7Buffer.append(T7['value'])
    P7Buffer.append(P7['value'])
    O1Buffer.append(O1['value'])
    O2Buffer.append(O2['value'])
    P8Buffer.append(P8['value'])
    T8Buffer.append(T8['value'])
    F8Buffer.append(F8['value'])
    AF4Buffer.append(AF4['value'])
    FC6Buffer.append(FC6['value'])
    F4Buffer.append(F4['value'])

if __name__ == "__main__":
    verify_user()
    load_dvs()
    main()
