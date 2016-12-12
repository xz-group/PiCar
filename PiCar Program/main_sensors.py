"""
main_sensors.py

Script that samples from encoders and IMU at 50Hz. Uses Twisted's LoopingCall function to call respective sampling method
every 20 milliseconds.
"""


import IMU, Encoder
import time
from twisted.internet import task, reactor

# Instantiate encoder and IMU objects (note encoder pins)
R_Enc = Encoder.Encoder(19,26)
L_Enc = Encoder.Encoder(6,13)
IMU1 = IMU.IMU()


def encRSample():
    timePre = time.time()
    sample = R_Enc.sample()
    timePost = time.time()
    outputFileEncR.write("%f\t%f\n" %(timePre, timePost))

def encLSample():
    timePre = time.time()
    sample = L_Enc.sample()
    timePost = time.time()
    outputFileEncL.write("%f\t%f\n" %(timePre, timePost))
    
def imuSample():
    timePre = time.time()
    sample = IMU1.sample()
    timePost = time.time()
    outputFileIMU.write("%f\t%f\n" %(timePre, timePost))

if __name__ == "__main__":
    
    #Outputs the time of start and end for each component sampling while the program is run
    outputFileIMU = open('imu-simul-results.txt', 'w+')
    outputFileEncR = open('encR-simul-results.txt', 'w+')
    outputFileEncL = open('encL-simul-results.txt', 'w+')

    l_imu = task.LoopingCall(imuSample)
    l_encr = task.LoopingCall(encRSample)
    l_encl = task.LoopingCall(encLSample)

    l_imu.start(0.02) #loops every 0.02s
    l_encr.start(0.02)
    l_encl.start(0.02)

    reactor.run()

    outputFileIMU.close()
    outputFileEncR.close()
    outputFileEncL.close()
    
    
