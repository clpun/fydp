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

headset = emotiv.Emotiv()
start_time = time.time()

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

'''def find_mean():
    counter = 0

    while counter < 100:
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

    print "F3 mean: "+str(f3_mean)
    print "FC5 mean: "+str(f3_mean)
    print "AF3 mean: "+str(f3_mean)
    print "F7 mean: "+str(f3_mean)
    print "T7 mean: "+str(f3_mean)
    print "P7 mean: "+str(f3_mean)
    print "O1 mean: "+str(f3_mean)
    print "O2 mean: "+str(f3_mean)
    print "P8 mean: "+str(f3_mean)
    print "T8 mean: "+str(f3_mean)
    print "F8 mean: "+str(f3_mean)
    print "AF4 mean: "+str(f3_mean)
    print "FC6 mean: "+str(f3_mean)
    print "F4 mean: "+str(f3_mean)
'''

def populate_csv_header():
    with open('fft_power_spectrum.csv', 'wb') as f:
        writer = csv.writer(f)
        header = ["Time (s)"]
        i = 0
        while i <= 45:
            header.append("f3_"+str(i)+"hz")
            i = i + 2.8125

        i = 0
        while i <= 45:
            header.append("fc5_"+str(i)+"hz")
            i = i + 2.8125

        i = 0
        while i <= 45:
            header.append("af3_"+str(i)+"hz")
            i = i + 2.8125

        i = 0
        while i <= 45:
            header.append("f7_"+str(i)+"hz")
            i = i + 2.8125

        i = 0
        while i <= 45:
            header.append("t7_"+str(i)+"hz")
            i = i + 2.8125

        i = 0
        while i <= 45:
            header.append("p7_"+str(i)+"hz")
            i = i + 2.8125

        i = 0
        while i <= 45:
            header.append("o1_"+str(i)+"hz")
            i = i + 2.8125

        i = 0
        while i <= 45:
            header.append("o2_"+str(i)+"hz")
            i = i + 2.8125

        i = 0
        while i <= 45:
            header.append("p8_"+str(i)+"hz")
            i = i + 2.8125

        i = 0
        while i <= 45:
            header.append("t8_"+str(i)+"hz")
            i = i + 2.8125

        i = 0
        while i <= 45:
            header.append("f8_"+str(i)+"hz")
            i = i + 2.8125

        i = 0
        while i <= 45:
            header.append("af4_"+str(i)+"hz")
            i = i + 2.8125

        i = 0
        while i <= 45:
            header.append("fc6_"+str(i)+"hz")
            i = i + 2.8125

        i = 0
        while i <= 45:
            header.append("fc6_"+str(i)+"hz")
            i = i + 2.8125

        writer.writerow(header)

def main():
    gevent.spawn(headset.setup)
    gevent.sleep(1)
    try:
        sample_counter = 0
        populate_csv_header()

        # Find mean
        #find_mean()

        # For building a finite time domain En to feed into CSP. 
        En = {
            'F3': [],
            'FC5': [],
            'AF3': [],
            'F7': [],
            'T7': [],
            'P7': [],
            'O1': [],
            'O2': [],
            'P8': [],
            'T8': [],
            'F8': [],
            'AF4': [],
            'FC6': [],
            'F4': []
        }

        print "Start!"
        
        # Run for 5 seconds
        loop_counter = 0
        trial_length = 32
        while loop_counter < trial_length:
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

            # Do FFT for each sensor after collecting 64 samples
            if sample_counter > 32:
                # Remove high frequency noise and dc offset
                F3Buffer_clean = sp.preprocess(F3Buffer, 8885.0)
                FC5Buffer_clean = sp.preprocess(FC5Buffer, 8885.0)
                AF3Buffer_clean = sp.preprocess(AF3Buffer, 8885.0)
                F7Buffer_clean = sp.preprocess(F7Buffer, 8885.0)
                T7Buffer_clean = sp.preprocess(T7Buffer, 8885.0)
                P7Buffer_clean = sp.preprocess(P7Buffer, 8885.0)
                O1Buffer_clean = sp.preprocess(O1Buffer, 8885.0)
                O2Buffer_clean = sp.preprocess(O2Buffer, 8885.0)
                P8Buffer_clean = sp.preprocess(P8Buffer, 8885.0)
                T8Buffer_clean = sp.preprocess(T8Buffer, 8885.0)
                F8Buffer_clean = sp.preprocess(F8Buffer, 8885.0)
                AF4Buffer_clean = sp.preprocess(AF4Buffer, 8885.0)
                FC6Buffer_clean = sp.preprocess(FC6Buffer, 8885.0)
                F4Buffer_clean = sp.preprocess(F4Buffer, 8885.0)

                # Put clean data into En
                for i in range(0, len(F3Buffer_clean)):
                    En['F3'].append(F3Buffer_clean[i])
                    En['FC5'].append(FC5Buffer_clean[i])
                    En['AF3'].append(AF3Buffer_clean[i])
                    En['F7'].append(F7Buffer_clean[i])
                    En['T7'].append(T7Buffer_clean[i])
                    En['P7'].append(P7Buffer_clean[i])
                    En['O1'].append(O1Buffer_clean[i])
                    En['O2'].append(O2Buffer_clean[i])
                    En['P8'].append(P8Buffer_clean[i])
                    En['T8'].append(T8Buffer_clean[i])
                    En['F8'].append(F8Buffer_clean[i])
                    En['AF4'].append(AF4Buffer_clean[i])
                    En['FC6'].append(FC6Buffer_clean[i])
                    En['F4'].append(F4Buffer_clean[i])

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
                fft_dict = {
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
                }

                # Write data set to a csv file
                fft.write_to_file(fft_dict, start_time)

                # Clear buffers
                clear_buffers()
                sample_counter = 0
                loop_counter = loop_counter + 1
            
            gevent.sleep(0)
        
        # Feed into CSP filter.
        e_matrix = csp.create_e_matrix(En, trial_length)
        sigma_matrix = csp.create_sigma_matrix(e_matrix, trial_length)
    except KeyboardInterrupt:
        headset.close()
    finally:
        headset.close()

if __name__ == "__main__":
    main()