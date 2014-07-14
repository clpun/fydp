from emokit import emotiv
import gevent

from scipy import fft, arange
import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":
    headset = emotiv.Emotiv()
    gevent.spawn(headset.setup)
    gevent.sleep(1)
    try:
        F3Buffer = []
        plt.ion()
        plt.show()

        sample_counter = 0

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

            # Print sensor data
            '''print "F3: "+str(F3)
            print "FC5: "+str(FC5)
            print "AF3: "+str(AF3)
            print "F7: "+str(F7)
            print "T7: "+str(T7)
            print "P7: "+str(P7)
            print "O1: "+str(O1)
            print "O2: "+str(O2)
            print "P8: "+str(P8)
            print "T8: "+str(T8)
            print "F8: "+str(F8)
            print "AF4: "+str(AF4)
            print "FC6: "+str(FC6)
            print "F4: "+str(F4)'''

            # Build buffers for FFT
            F3Buffer.append(F3)
            sample_counter = sample_counter + 1

            # Do FFT for each sensor after collecting 64 samples
            if sample_counter > 64:
                plt.clf()

                # FFT for F3
                F3NumpyArray = np.array(F3Buffer)
                y = fft(F3NumpyArray)

                n = len(y) # length of the signal
                k = arange(n)
                T = n/128.0
                frq = k/T # two sides frequency range
                frq = frq[range(n/2)] # one side frequency range

                Y = (y/float(n))*2.0 # fft computing and normalization
                Y = Y[range(n/2)]
                
                # Plot FFT for F3
                plt.plot(frq,abs(Y),'r') # plotting the spectrum
                plt.xlabel('Freq (Hz)')
                plt.ylabel('|Y(freq)|')
                plt.draw()

                # Clear buffers
                del F3Buffer[:]
                sample_counter = 0

            gevent.sleep(0)

    except KeyboardInterrupt:
        headset.close()
    finally:
        headset.close()
