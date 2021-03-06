import sys
#sys.path.append("..")
from ..lib import emotiv
import gevent
import numpy as np
import signal_preprocessing as sp
import fft
import math

class UserPreference:
    user_name = "User"
    env_offset_avg_var = {}
    def write_env_offset_avg_var(self,name,var):
        self.env_offset_avg_var.update({name: var})

    def read_env_offset_avg_var(self,name):
        return self.env_offset_avg_var[name]


user_preference = UserPreference()
f3_mean = 0.0
fc5_mean = 0.0
af3_mean = 0.0
f7_mean = 0.0
t7_mean = 0.0
p7_mean = 0.0
o1_mean = 0.0
o2_mean = 0.0
p8_mean = 0.0
t8_mean = 0.0
f8_mean = 0.0
af4_mean = 0.0
fc6_mean = 0.0
f4_mean = 0.0
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

sensor_names = ['F3', 'FC5', 'AF3', 'F7', 'T7', 'P7', 'O1', 'O2', 'P8', 'T8', 'F8', 'AF4', 'FC6', 'F4']
data = {}
samplingFreq = 128.0
fftSamplingNum = 26.0
oneFftPeriod = fftSamplingNum/samplingFreq
index = 0
test_duration = 15.0 # seconds
durationIndex = math.ceil(test_duration/oneFftPeriod)

def calculate_tf():
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
        for ii in range(0,len(data)-1):
            slice_iaf = data[ii][sensor][7]
            min_iaf = 7
            for jj in range(8,13):
                if data[ii][sensor][jj] >= slice_iaf:
                    min_iaf = jj
                    slice_iaf = data[ii][sensor][jj]
            iaf += int(min_iaf)
        iaf_matrix[sensor] = int(iaf/float(len(data)))
        #Find tf
        for ii in range(0,len(data)-1):
            for jj in range(4,iaf_matrix[sensor]-1):
                expectation[str(jj)] += data[ii][sensor][jj]
                expectationSquared[str(jj)] += (data[ii][sensor][jj])**2

        for jj in range(4,iaf_matrix[sensor]-1):
            expectation[str(jj)] /= float(len(data))
            expectationSquared[str(jj)] /= float(len(data))
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

def main():
    global headset
    global data
    global gyroX
    global gyroY
    global battery
    global index

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
        while index <= durationIndex:
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

                # Calculate the magnitude sum of the 5 frequency bands.
                # Delta = 1-3 Hz [0:3]
                # Theta = 4-7 Hz [4:7]
                # Alpha = 8-15 Hz [8:15]
                # Beta = 16-31 Hz [16:31]
                # Gamma = 32-64 Hz [32:-1]

                # theta_avg = {}
                # alpha_avg = {}
                data[index] = {}
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

                    data[index][sensor] = fft_comp

                # Clear buffers
                clear_buffers()
                sample_counter = 0
                index += 1

            
            gevent.sleep(0)

        calculate_tf()
    except KeyboardInterrupt:
        headset.close()
    finally:
        headset.close()

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

if __name__ == "__main__":
    main()