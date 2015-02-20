import sys
#sys.path.append("..")
from ..lib import emotiv
import gevent
import numpy as np
import csv
import time
import os

import select
import fft
import signal_preprocessing as sp
import check_signal_quality

fftSamplingNum = 26

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

# Control Variables
start_recording = True

# Variables for the sum magnitude of the 5 frequency bands.
delta_sum_mag = {}
theta_sum_mag = {}
alpha_sum_mag = {}
beta_sum_mag = {}
gamma_sum_mag = {}

band_types = ['delta', 'theta', 'alpha', 'beta', 'gamma']
sensor_names = ['F3', 'FC5', 'AF3', 'F7', 'T7', 'P7', 'O1', 'O2', 'P8', 'T8', 'F8', 'AF4', 'FC6', 'F4']

# Variables for determining if a frequency band has steady increase in F3
f3_delta_prev_mag = 0
f3_delta_count = 0
o1_alpha_prev_mag = 0
o1_beta_prev_mag = 0
o1_theta_prev_mag = 0
o1_delta_prev_mag = 0
o1_gamma_prev_mag = 0
o2_alpha_prev_mag = 0
o2_beta_prev_mag = 0
o2_theta_prev_mag = 0
o2_delta_prev_mag = 0
o2_gamma_prev_mag = 0
o1_alpha_count = 0
o1_beta_count = 0
o1_theta_count = 0
o1_delta_count = 0
o1_gamma_count = 0
o2_alpha_count = 0
o2_beta_count = 0
o2_theta_count = 0
o2_delta_count = 0
o2_gamma_count = 0

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
    headset = emotiv.Emotiv()
    gevent.spawn(headset.setup)
    gevent.sleep(1)
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
    global f3_delta_prev_mag
    global f3_delta_count
    global o1_alpha_prev_mag
    global o1_beta_prev_mag
    global o1_theta_prev_mag
    global o1_delta_prev_mag
    global o1_gamma_prev_mag
    global o2_alpha_prev_mag
    global o2_beta_prev_mag
    global o2_theta_prev_mag
    global o2_delta_prev_mag
    global o2_gamma_prev_mag
    global o1_alpha_count
    global o1_beta_count
    global o1_theta_count
    global o1_delta_count
    global o1_gamma_count
    global o2_alpha_count
    global o2_beta_count
    global o2_theta_count
    global o2_delta_count
    global o2_gamma_count

    if(gamma_sum_mag['O1'] > o1_gamma_prev_mag):
        #print "O1 gamma increase; mag = {0}".format(gamma_sum_mag['O1'])
        o1_gamma_count += 1
    else:
        o1_gamma_count = 0
    if(gamma_sum_mag['O2'] > o2_gamma_prev_mag):
        #print "O2 gamma increase; mag = {0}".format(gamma_sum_mag['O2'])
        o2_gamma_count += 1
    else:
        o2_gamma_count = 0

    if o1_gamma_count >= 3:
        #print "**O1 gamma increase; mag = {0}, ({1})".format(gamma_sum_mag['O1'],gamma_sum_mag['O1'] - o1_gamma_prev_mag)
        pass
    if o2_gamma_count >= 3:
        #print "**O2 gamma increase; mag = {0}, ({1})".format(gamma_sum_mag['O2'],gamma_sum_mag['O2'] - o2_gamma_prev_mag)
        pass

    #print "O1 gamma: mag = {0}, ({1})\nO2 gamma: mag = {2}, ({3})".format(int(gamma_sum_mag['O1']),int(gamma_sum_mag['O1'] - o1_gamma_prev_mag),int(gamma_sum_mag['O2']),int(gamma_sum_mag['O2'] - o2_gamma_prev_mag))

    o1_gamma_prev_mag = gamma_sum_mag['O1']
    o2_gamma_prev_mag = gamma_sum_mag['O2']
    #print "--------------------"

def main():
    global headset

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

    headset = emotiv.Emotiv()
    gevent.spawn(headset.setup)
    gevent.sleep(1)

    try:
        sample_counter = 0

        print '~~~~~~~~~~~'
        while True:
            # Retrieve emotiv packet
            packet = headset.dequeue()
            # print str(packet)
            #for key in packet.sensors.keys():
            #    print str(key) + " = " + str(packet.sensors[key])
            #print ""

            # Get contact quality data
            #F3_quality = packet.sensors['F3']['quality']
            #FC5_quality = packet.sensors['FC5']['quality']
            #AF3_quality = packet.sensors['AF3']['quality']
            #F7_quality = packet.sensors['F7']['quality']
            #T7_quality = packet.sensors['T7']['quality']
            #P7_quality = packet.sensors['P7']['quality']
            #O1_quality = packet.sensors['O1']['quality']
            #O2_quality = packet.sensors['O2']['quality']
            #P8_quality = packet.sensors['P8']['quality']
            #T8_quality = packet.sensors['T8']['quality']
            #F8_quality = packet.sensors['F8']['quality']
            #AF4_quality = packet.sensors['AF4']['quality']
            #FC6_quality = packet.sensors['FC6']['quality']
            #F4_quality = packet.sensors['F4']['quality']

            # Get sensor data
            #F3 = packet.sensors['F3']['value']
            #FC5 = packet.sensors['FC5']['value']
            #AF3 = packet.sensors['AF3']['value']
            #F7 = packet.sensors['F7']['value']
            #T7 = packet.sensors['T7']['value']
            #P7 = packet.sensors['P7']['value']
            #O1 = packet.sensors['O1']['value']
            #O2 = packet.sensors['O2']['value']
            #P8 = packet.sensors['P8']['value']
            #T8 = packet.sensors['T8']['value']
            #F8 = packet.sensors['F8']['value']
            #AF4 = packet.sensors['AF4']['value']
            #FC6 = packet.sensors['FC6']['value']
            #F4 = packet.sensors['F4']['value']

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

            #print "F3 = " + str(F3)
            #print "FC5 = " + str(FC5)
            #print "AF3 = " + str(AF3)
            #print "F7 = " + str(F7)
            #print "F8 = " + str(F8)
            #print "F4 = " + str(F4)
            #print ""

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

            sample_counter = sample_counter + 1

            # Do FFT for each sensor after collecting 32 samples
            if sample_counter > fftSamplingNum:
                # Remove high frequency noise and dc offset
                F3Buffer_clean = sp.preprocess(F3Buffer, f3_mean)
                FC5Buffer_clean = sp.preprocess(FC5Buffer, fc5_mean)
                AF3Buffer_clean = sp.preprocess(AF3Buffer, af3_mean)
                F7Buffer_clean = sp.preprocess(F7Buffer, f7_mean)
                T7Buffer_clean = sp.preprocess(T7Buffer, t7_mean)
                P7Buffer_clean = sp.preprocess(P7Buffer, p7_mean)
                O1Buffer_clean = sp.preprocess(O1Buffer, o1_mean)
                O2Buffer_clean = sp.preprocess(O2Buffer, o2_mean)
                P8Buffer_clean = sp.preprocess(P8Buffer, p8_mean)
                T8Buffer_clean = sp.preprocess(T8Buffer, t8_mean)
                F8Buffer_clean = sp.preprocess(F8Buffer, f8_mean)
                AF4Buffer_clean = sp.preprocess(AF4Buffer, af4_mean)
                FC6Buffer_clean = sp.preprocess(FC6Buffer, fc6_mean)
                F4Buffer_clean = sp.preprocess(F4Buffer, f4_mean)

                # Apply DFT to extract frequency components
                f3_fft = fft.compute_fft(F3Buffer_clean)
                fc5_fft = fft.compute_fft(FC5Buffer_clean)
                af3_fft = fft.compute_fft(AF3Buffer_clean)
                f7_fft = fft.compute_fft(F7Buffer_clean)
                t7_fft = fft.compute_fft(T7Buffer_clean)
                p7_fft = fft.compute_fft(P7Buffer_clean)
                o1_fft = fft.compute_fft(O1Buffer_clean)
                o2_fft = fft.compute_fft(O2Buffer_clean)
                p8_fft = fft.compute_fft(P8Buffer_clean)
                t8_fft = fft.compute_fft(T8Buffer_clean)
                f8_fft = fft.compute_fft(F8Buffer_clean)
                af4_fft = fft.compute_fft(AF4Buffer_clean)
                fc6_fft = fft.compute_fft(FC6Buffer_clean)
                f4_fft = fft.compute_fft(F4Buffer_clean)

                # Build dictionary
                '''fft_dict = {
                    'F3': f3_fft,
                    'FC5': fc5_fft,
                    'AF3': af3_fft,
                    'F7': f7_fft,
                    'T7': t7_fft,
                    'P7': p7_fft,
                    'O1': o1_fft,
                    'O2': o2_fft,
                    'P8': p8_fft,
                    'T8': t8_fft,
                    'F8': f8_fft,
                    'AF4': af4_fft,
                    'FC6': fc6_fft,
                    'F4': f4_fft
                }'''

                # Calculate the magnitude sum of the 5 frequency bands.
                # Delta = 1-3 Hz [0:3]
                # Theta = 4-7 Hz [4:7]
                # Alpha = 8-15 Hz [8:15]
                # Beta = 16-31 Hz [16:31]
                # Gamma = 32-64 Hz [32:-1]
                delta_sum_mag['F3'] = sum(f3_fft[0:3])
                delta_sum_mag['FC5'] = sum(fc5_fft[0:3])
                delta_sum_mag['AF3'] = sum(af3_fft[0:3])
                delta_sum_mag['F7'] = sum(f7_fft[0:3])
                delta_sum_mag['T7'] = sum(t7_fft[0:3])
                delta_sum_mag['P7'] = sum(p7_fft[0:3])
                delta_sum_mag['O1'] = sum(o1_fft[0:3])
                delta_sum_mag['O2'] = sum(o2_fft[0:3])
                delta_sum_mag['P8'] = sum(p8_fft[0:3])
                delta_sum_mag['T8'] = sum(t8_fft[0:3])
                delta_sum_mag['F8'] = sum(f8_fft[0:3])
                delta_sum_mag['AF4'] = sum(af4_fft[0:3])
                delta_sum_mag['FC6'] = sum(fc6_fft[0:3])
                delta_sum_mag['F4'] = sum(f4_fft[0:3])

                theta_sum_mag['F3'] = sum(f3_fft[4:7])
                theta_sum_mag['FC5'] = sum(fc5_fft[4:7])
                theta_sum_mag['AF3'] = sum(af3_fft[4:7])
                theta_sum_mag['F7'] = sum(f7_fft[4:7])
                theta_sum_mag['T7'] = sum(t7_fft[4:7])
                theta_sum_mag['P7'] = sum(p7_fft[4:7])
                theta_sum_mag['O1'] = sum(o1_fft[4:7])
                theta_sum_mag['O2'] = sum(o2_fft[4:7])
                theta_sum_mag['P8'] = sum(p8_fft[4:7])
                theta_sum_mag['T8'] = sum(t8_fft[4:7])
                theta_sum_mag['F8'] = sum(f8_fft[4:7])
                theta_sum_mag['AF4'] = sum(af4_fft[4:7])
                theta_sum_mag['FC6'] = sum(fc6_fft[4:7])
                theta_sum_mag['F4'] = sum(f4_fft[4:7])

                alpha_sum_mag['F3'] = sum(f3_fft[8:15])
                alpha_sum_mag['FC5'] = sum(fc5_fft[8:15])
                alpha_sum_mag['AF3'] = sum(af3_fft[8:15])
                alpha_sum_mag['F7'] = sum(f7_fft[8:15])
                alpha_sum_mag['T7'] = sum(t7_fft[8:15])
                alpha_sum_mag['P7'] = sum(p7_fft[8:15])
                alpha_sum_mag['O1'] = sum(o1_fft[8:15])
                alpha_sum_mag['O2'] = sum(o2_fft[8:15])
                alpha_sum_mag['P8'] = sum(p8_fft[8:15])
                alpha_sum_mag['T8'] = sum(t8_fft[8:15])
                alpha_sum_mag['F8'] = sum(f8_fft[8:15])
                alpha_sum_mag['AF4'] = sum(af4_fft[8:15])
                alpha_sum_mag['FC6'] = sum(fc6_fft[8:15])
                alpha_sum_mag['F4'] = sum(f4_fft[8:15])

                beta_sum_mag['F3'] = sum(f3_fft[16:31])
                beta_sum_mag['FC5'] = sum(fc5_fft[16:31])
                beta_sum_mag['AF3'] = sum(af3_fft[16:31])
                beta_sum_mag['F7'] = sum(f7_fft[16:31])
                beta_sum_mag['T7'] = sum(t7_fft[16:31])
                beta_sum_mag['P7'] = sum(p7_fft[16:31])
                beta_sum_mag['O1'] = sum(o1_fft[16:31])
                beta_sum_mag['O2'] = sum(o2_fft[16:31])
                beta_sum_mag['P8'] = sum(p8_fft[16:31])
                beta_sum_mag['T8'] = sum(t8_fft[16:31])
                beta_sum_mag['F8'] = sum(f8_fft[16:31])
                beta_sum_mag['AF4'] = sum(af4_fft[16:31])
                beta_sum_mag['FC6'] = sum(fc6_fft[16:31])
                beta_sum_mag['F4'] = sum(f4_fft[16:31])

                gamma_sum_mag['F3'] = sum(f3_fft[32:])
                gamma_sum_mag['FC5'] = sum(fc5_fft[32:])
                gamma_sum_mag['AF3'] = sum(af3_fft[32:])
                gamma_sum_mag['F7'] = sum(f7_fft[32:])
                gamma_sum_mag['T7'] = sum(t7_fft[32:])
                gamma_sum_mag['P7'] = sum(p7_fft[32:])
                gamma_sum_mag['O1'] = sum(o1_fft[32:])
                gamma_sum_mag['O2'] = sum(o2_fft[32:])
                gamma_sum_mag['P8'] = sum(p8_fft[32:])
                gamma_sum_mag['T8'] = sum(t8_fft[32:])
                gamma_sum_mag['F8'] = sum(f8_fft[32:])
                gamma_sum_mag['AF4'] = sum(af4_fft[32:])
                gamma_sum_mag['FC6'] = sum(fc6_fft[32:])
                gamma_sum_mag['F4'] = sum(f4_fft[32:])

                '''
                print "Delta Magnitude Sum:"
                for key in delta_sum_mag.keys():
                    print key, ":", delta_sum_mag[key]
                print ""

                print "Alpha Magnitude Sum:"
                for key in alpha_sum_mag.keys():
                    print key, ":", alpha_sum_mag[key]
                print ""

                print "Beta Magnitude Sum:"
                for key in beta_sum_mag.keys():
                    print key, ":", beta_sum_mag[key]
                print ""

                print "Gamma Magnitude Sum:"
                for key in gamma_sum_mag.keys():
                    print key, ":", gamma_sum_mag[key]
                print ""
                '''

                # Determine if a freq band of a channel has a steady increase in magnitude over 3 ffts
                analyze_pattern()
                power_dict = {}
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

                power_dict['quality'] = {}
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

                print "printing time for every emit = "+str(time.time())
                yield power_dict

                # Clear buffers
                clear_buffers()
                sample_counter = 0

            gevent.sleep(0)

    except KeyboardInterrupt:
        headset.close()
    finally:
        headset.close()

if __name__ == "__main__":
    main()
