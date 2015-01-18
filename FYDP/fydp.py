import sys
sys.path.append("..")
import emotiv
import gevent
import numpy as np
import csv
import time

import fft
import signal_preprocessing as sp
import CSP as csp
import check_signal_quality

headset = emotiv.Emotiv()
start_time = time.time()

# Variables for the sum magnitude of the 5 frequency bands. 
delta_sum_mag = {}
theta_sum_mag = {}
alpha_sum_mag = {}
beta_sum_mag = {}
gamma_sum_mag = {}

# Variables for determining if a frequency band has steady increase in F3 
f3_delta_prev_mag = 0
f3_delta_count = 0

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
    counter = 0

    while counter < 1000:
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

        counter = counter + 1

    global f3_mean
    f3_mean = np.mean(F3Buffer)
    global fc5_mean
    fc5_mean = np.mean(FC5Buffer)
    global af3_mean
    af3_mean = np.mean(AF3Buffer)
    global f7_mean
    f7_mean = np.mean(F7Buffer)
    global t7_mean
    t7_mean = np.mean(T7Buffer)
    global p7_mean
    p7_mean = np.mean(P7Buffer)
    global o1_mean
    o1_mean = np.mean(O1Buffer)
    global o2_mean
    o2_mean = np.mean(O2Buffer)
    global p8_mean
    p8_mean = np.mean(P8Buffer)
    global t8_mean
    t8_mean = np.mean(T8Buffer)
    global f8_mean
    f8_mean = np.mean(F8Buffer)
    global af4_mean
    af4_mean = np.mean(AF4Buffer)
    global fc6_mean
    fc6_mean = np.mean(FC6Buffer)
    global f4_mean
    f4_mean = np.mean(F4Buffer)

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

def main():
    global f3_delta_prev_mag
    global f3_delta_count
    
    gevent.spawn(headset.setup)
    gevent.sleep(1)
    try:
        sample_counter = 0
        #populate_csv_header()

        # Find mean
        print "Calculating signal average. Please wait..."
        find_mean()

        print "Please check the quality of signals. "
        check_signal_quality.run(headset)

        raw_input("Please press enter when you are ready to start. ")

        print "Start!"
        
        # Run for 5 seconds
        #loop_counter = 0
        #trial_length = 32
        while True:
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
                # Delta = 1-4 [0:1]
                # Theta = 4-7 [?]
                # Alpha = 7-13 [2:3]
                # Beta = 13-30 [4:7]
                # Gamma = 30-64 [8:-1]
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

                alpha_sum_mag['F3'] = sum(f3_fft[2:3])
                alpha_sum_mag['FC5'] = sum(fc5_fft[2:3])
                alpha_sum_mag['AF3'] = sum(af3_fft[2:3])
                alpha_sum_mag['F7'] = sum(f7_fft[2:3])
                alpha_sum_mag['T7'] = sum(t7_fft[2:3])
                alpha_sum_mag['P7'] = sum(p7_fft[2:3])
                alpha_sum_mag['O1'] = sum(o1_fft[2:3])
                alpha_sum_mag['O2'] = sum(o2_fft[2:3])
                alpha_sum_mag['P8'] = sum(p8_fft[2:3])
                alpha_sum_mag['T8'] = sum(t8_fft[2:3])
                alpha_sum_mag['F8'] = sum(f8_fft[2:3])
                alpha_sum_mag['AF4'] = sum(af4_fft[2:3])
                alpha_sum_mag['FC6'] = sum(fc6_fft[2:3])
                alpha_sum_mag['F4'] = sum(f4_fft[2:3])

                beta_sum_mag['F3'] = sum(f3_fft[4:7])
                beta_sum_mag['FC5'] = sum(fc5_fft[4:7])
                beta_sum_mag['AF3'] = sum(af3_fft[4:7])
                beta_sum_mag['F7'] = sum(f7_fft[4:7])
                beta_sum_mag['T7'] = sum(t7_fft[4:7])
                beta_sum_mag['P7'] = sum(p7_fft[4:7])
                beta_sum_mag['O1'] = sum(o1_fft[4:7])
                beta_sum_mag['O2'] = sum(o2_fft[4:7])
                beta_sum_mag['P8'] = sum(p8_fft[4:7])
                beta_sum_mag['T8'] = sum(t8_fft[4:7])
                beta_sum_mag['F8'] = sum(f8_fft[4:7])
                beta_sum_mag['AF4'] = sum(af4_fft[4:7])
                beta_sum_mag['FC6'] = sum(fc6_fft[4:7])
                beta_sum_mag['F4'] = sum(f4_fft[4:7])

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

                # Determine if a frequency band of F3 has a steady increase in magnitude over 5 ffts
                if (delta_sum_mag['F3'] > f3_delta_prev_mag):
                    print "F3 delta increasing in magnitude! mag = {0}".format(delta_sum_mag['F3'])
                    f3_delta_count += 1
                else:
                    f3_delta_count = 0
                f3_delta_prev_mag = delta_sum_mag['F3']

                if f3_delta_count >= 5:
                    print "F3 delta has a steady increase in magnitude"

                # Clear buffers
                clear_buffers()
                sample_counter = 0
                #loop_counter = loop_counter + 1
            
            gevent.sleep(0)
        
    except KeyboardInterrupt:
        headset.close()
    finally:
        headset.close()

if __name__ == "__main__":
    main()