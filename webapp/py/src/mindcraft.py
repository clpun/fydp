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
#import check_signal_quality

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
start_streaming = True
start_recording = True

# Variables for the sum magnitude of the 5 frequency bands. 
delta_sum_mag = {}
theta_sum_mag = {}
alpha_sum_mag = {}
beta_sum_mag = {}
gamma_sum_mag = {}

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

def set_developer_mode():
    print 'Setting up for Developer mode'
    for path in sys.path:
        print 'sys.path = ' + path
    direc = dir(devapp)
    for d in direc:
        print 'devapp dir = ' + d

def stop_streaming():
    # print "mindcraft log : Stop Streaming Live Data"
    start_streaming = False

def get_userid():
    print 'request id = '+str(user_preference.user_name)
    return str(user_preference.user_name)

def verify_user():
    global user_preference
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
                # for key in user_preference.env_offset_avg_var:
                #     try:
                #         if 
                #             user_verify = True
                #         if float(user_preference.env_offset_avg_var[key]) <= 0:
                #             user_verify = False
                #     except:
                #         user_verify = False
                if not user_verify:
                    print "Something is wrong with the environment offset average variables. Please use another user id."
                else:
                    if server_testing_mode:
                        # devapp.f3_mean = f3_mean
                        # devapp.fc5_mean = fc5_mean
                        # devapp.af3_mean = af3_mean
                        # devapp.f7_mean = f7_mean
                        # devapp.t7_mean = t7_mean
                        # devapp.p7_mean = p7_mean
                        # devapp.o1_mean = o1_mean
                        # devapp.o2_mean = o2_mean
                        # devapp.p8_mean = p8_mean
                        # devapp.t8_mean = t8_mean
                        # devapp.f8_mean = f8_mean
                        # devapp.af4_mean = af4_mean
                        # devapp.fc6_mean = fc6_mean
                        # devapp.f4_mean = f4_mean
                        # devapi.write_userid(user_preference.user_name)
                        pass
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
    counter = 0

    raw_input("Need to Calculate signal average. Do NOT wear the headset. Please press enter to continue...")
    print("Calculating signal average. Please wait...")

    while counter < 1000:
        # Retrieve emotiv packet
        headset = emotiv.Emotiv()
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

def populate_csv_header():
    with open('fft_mag_spectrum_formatted.csv', 'wb') as f:
        writer = csv.writer(f)
        header = ["Time (s)"]
        i = 0
        while i <= 63:
            header.append("f3_"+str(i)+"hz")
            i = i + 3.87878788

        i = 0
        while i <= 63:
            header.append("fc5_"+str(i)+"hz")
            i = i + 3.87878788

        i = 0
        while i <= 63:
            header.append("af3_"+str(i)+"hz")
            i = i + 3.87878788

        i = 0
        while i <= 63:
            header.append("f7_"+str(i)+"hz")
            i = i + 3.87878788

        i = 0
        while i <= 63:
            header.append("t7_"+str(i)+"hz")
            i = i + 3.87878788

        i = 0
        while i <= 63:
            header.append("p7_"+str(i)+"hz")
            i = i + 3.87878788

        i = 0
        while i <= 63:
            header.append("o1_"+str(i)+"hz")
            i = i + 3.87878788

        i = 0
        while i <= 63:
            header.append("o2_"+str(i)+"hz")
            i = i + 3.87878788

        i = 0
        while i <= 63:
            header.append("p8_"+str(i)+"hz")
            i = i + 3.87878788

        i = 0
        while i <= 63:
            header.append("t8_"+str(i)+"hz")
            i = i + 3.87878788

        i = 0
        while i <= 63:
            header.append("f8_"+str(i)+"hz")
            i = i + 3.87878788

        i = 0
        while i <= 63:
            header.append("af4_"+str(i)+"hz")
            i = i + 3.87878788

        i = 0
        while i <= 63:
            header.append("fc6_"+str(i)+"hz")
            i = i + 3.87878788

        i = 0
        while i <= 63:
            header.append("fc6_"+str(i)+"hz")
            i = i + 3.87878788

        writer.writerow(header)

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
    if server_testing_mode:
        #set_developer_mode()
        while True:
            gevent.sleep(0.250)
            rand_val = random.randrange(0,8000,1)
            test_data = {'delta':{'F3':rand_val,'FC5':rand_val,'AF3':rand_val,'F7':rand_val,'T7':rand_val,'P7':rand_val,'O1':rand_val,'O2':rand_val,'P8':rand_val,'T8':rand_val,'F8':rand_val,'AF4':rand_val,'FC6':rand_val,'F4':rand_val},
                'theta':{'F3':rand_val,'FC5':rand_val,'AF3':rand_val,'F7':rand_val,'T7':rand_val,'P7':rand_val,'O1':rand_val,'O2':rand_val,'P8':rand_val,'T8':rand_val,'F8':rand_val,'AF4':rand_val,'FC6':rand_val,'F4':rand_val},
                'alpha':{'F3':rand_val,'FC5':rand_val,'AF3':rand_val,'F7':rand_val,'T7':rand_val,'P7':rand_val,'O1':rand_val,'O2':rand_val,'P8':rand_val,'T8':rand_val,'F8':rand_val,'AF4':rand_val,'FC6':rand_val,'F4':rand_val},
                'beta':{'F3':rand_val,'FC5':rand_val,'AF3':rand_val,'F7':rand_val,'T7':rand_val,'P7':rand_val,'O1':rand_val,'O2':rand_val,'P8':rand_val,'T8':rand_val,'F8':rand_val,'AF4':rand_val,'FC6':rand_val,'F4':rand_val},
                'gamma':{'F3':rand_val,'FC5':rand_val,'AF3':rand_val,'F7':rand_val,'T7':rand_val,'P7':rand_val,'O1':rand_val,'O2':rand_val,'P8':rand_val,'T8':rand_val,'F8':rand_val,'AF4':rand_val,'FC6':rand_val,'F4':rand_val}
            }
            #print str(test_data)
            print "Server Testing Mode: print timestamp for every emit of testdata({0}) = {1}".format(str(rand_val),str(time.time()))
            yield test_data

    global start_streaming
    start_streaming = True
    headset = emotiv.Emotiv()
    gevent.spawn(headset.setup)
    gevent.sleep(1)
    global start_recording
    start_recording = True
    verify_user() 
    
    try:
        sample_counter = 0

        #print "Please check the quality of signals. "
        #check_signal_quality.run(headset)

        print '~~~~~~~~~~~'
        while start_streaming:
            if not start_recording:
                prompt_start_recording = raw_input("Press any Keys to Start Recording\n")
                start_recording = True
            else:
                #try:
                    # Retrieve emotiv packet
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

                    sample_counter = sample_counter + 1

                    # Do FFT for each sensor after collecting 32 samples
                    if sample_counter > 32:
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

                        # Write data set to a csv file
                        #fft.write_to_file(fft_dict, start_time)

                        # Calculate the magnitude sum of the 5 frequency bands.
                        # Delta = 1-4 Hz [0]
                        # Theta = 4-7 Hz [1:2]
                        # Alpha = 7-13 Hz [3:4]
                        # Beta = 13-30 Hz [5:7]
                        # Gamma = 30-64 Hz [8:-1]
                        delta_sum_mag['F3'] = sum(f3_fft[0:1])
                        delta_sum_mag['FC5'] = sum(fc5_fft[0:1])
                        delta_sum_mag['AF3'] = sum(af3_fft[0:1])
                        delta_sum_mag['F7'] = sum(f7_fft[0:1])
                        delta_sum_mag['T7'] = sum(t7_fft[0:1])
                        delta_sum_mag['P7'] = sum(p7_fft[0:1])
                        delta_sum_mag['O1'] = sum(o1_fft[0:1])
                        delta_sum_mag['O2'] = sum(o2_fft[0:1])
                        delta_sum_mag['P8'] = sum(p8_fft[0:1])
                        delta_sum_mag['T8'] = sum(t8_fft[0:1])
                        delta_sum_mag['F8'] = sum(f8_fft[0:1])
                        delta_sum_mag['AF4'] = sum(af4_fft[0:1])
                        delta_sum_mag['FC6'] = sum(fc6_fft[0:1])
                        delta_sum_mag['F4'] = sum(f4_fft[0:1])

                        theta_sum_mag['F3'] = sum(f3_fft[1:2])
                        theta_sum_mag['FC5'] = sum(fc5_fft[1:2])
                        theta_sum_mag['AF3'] = sum(af3_fft[1:2])
                        theta_sum_mag['F7'] = sum(f7_fft[1:2])
                        theta_sum_mag['T7'] = sum(t7_fft[1:2])
                        theta_sum_mag['P7'] = sum(p7_fft[1:2])
                        theta_sum_mag['O1'] = sum(o1_fft[1:2])
                        theta_sum_mag['O2'] = sum(o2_fft[1:2])
                        theta_sum_mag['P8'] = sum(p8_fft[1:2])
                        theta_sum_mag['T8'] = sum(t8_fft[1:2])
                        theta_sum_mag['F8'] = sum(f8_fft[1:2])
                        theta_sum_mag['AF4'] = sum(af4_fft[1:2])
                        theta_sum_mag['FC6'] = sum(fc6_fft[1:2])
                        theta_sum_mag['F4'] = sum(f4_fft[1:2])

                        alpha_sum_mag['F3'] = sum(f3_fft[3:4])
                        alpha_sum_mag['FC5'] = sum(fc5_fft[3:4])
                        alpha_sum_mag['AF3'] = sum(af3_fft[3:4])
                        alpha_sum_mag['F7'] = sum(f7_fft[3:4])
                        alpha_sum_mag['T7'] = sum(t7_fft[3:4])
                        alpha_sum_mag['P7'] = sum(p7_fft[3:4])
                        alpha_sum_mag['O1'] = sum(o1_fft[3:4])
                        alpha_sum_mag['O2'] = sum(o2_fft[3:4])
                        alpha_sum_mag['P8'] = sum(p8_fft[3:4])
                        alpha_sum_mag['T8'] = sum(t8_fft[3:4])
                        alpha_sum_mag['F8'] = sum(f8_fft[3:4])
                        alpha_sum_mag['AF4'] = sum(af4_fft[3:4])
                        alpha_sum_mag['FC6'] = sum(fc6_fft[3:4])
                        alpha_sum_mag['F4'] = sum(f4_fft[3:4])

                        beta_sum_mag['F3'] = sum(f3_fft[5:7])
                        beta_sum_mag['FC5'] = sum(fc5_fft[5:7])
                        beta_sum_mag['AF3'] = sum(af3_fft[5:7])
                        beta_sum_mag['F7'] = sum(f7_fft[5:7])
                        beta_sum_mag['T7'] = sum(t7_fft[5:7])
                        beta_sum_mag['P7'] = sum(p7_fft[5:7])
                        beta_sum_mag['O1'] = sum(o1_fft[5:7])
                        beta_sum_mag['O2'] = sum(o2_fft[5:7])
                        beta_sum_mag['P8'] = sum(p8_fft[5:7])
                        beta_sum_mag['T8'] = sum(t8_fft[5:7])
                        beta_sum_mag['F8'] = sum(f8_fft[5:7])
                        beta_sum_mag['AF4'] = sum(af4_fft[5:7])
                        beta_sum_mag['FC6'] = sum(fc6_fft[5:7])
                        beta_sum_mag['F4'] = sum(f4_fft[5:7])

                        gamma_sum_mag['F3'] = sum(f3_fft[8:])
                        gamma_sum_mag['FC5'] = sum(fc5_fft[8:])
                        gamma_sum_mag['AF3'] = sum(af3_fft[8:])
                        gamma_sum_mag['F7'] = sum(f7_fft[8:])
                        gamma_sum_mag['T7'] = sum(t7_fft[8:])
                        gamma_sum_mag['P7'] = sum(p7_fft[8:])
                        gamma_sum_mag['O1'] = sum(o1_fft[8:])
                        gamma_sum_mag['O2'] = sum(o2_fft[8:])
                        gamma_sum_mag['P8'] = sum(p8_fft[8:])
                        gamma_sum_mag['T8'] = sum(t8_fft[8:])
                        gamma_sum_mag['F8'] = sum(f8_fft[8:])
                        gamma_sum_mag['AF4'] = sum(af4_fft[8:])
                        gamma_sum_mag['FC6'] = sum(fc6_fft[8:])
                        gamma_sum_mag['F4'] = sum(f4_fft[8:])

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
                        power_dict = {'delta':delta_sum_mag,'theta':theta_sum_mag,'alpha':alpha_sum_mag,'beta':beta_sum_mag,'gamma':gamma_sum_mag}
                        #s = str(devapi.get_all_power())
                        #print str(power_dict)
                        print "printing time for every emit = "+str(time.time())
                        yield power_dict
                        
                        # Clear buffers
                        clear_buffers()
                        sample_counter = 0
                # except:
                #     pass

                # i,o,e = select.select([sys.stdin],[],[],0.0001)
                # for s in i:
                #     if s == sys.stdin:
                #         #print 'key detected'
                #         sys.stdin.readline()
                #         start_recording = False
                #         clear_buffers()
                #         sample_counter = 0

            gevent.sleep(0)
        
    except KeyboardInterrupt:
        headset.close()
    finally:
        headset.close()

if __name__ == "__main__":
    main()