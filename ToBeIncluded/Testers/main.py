import IMU
import Encoder
import time
from twisted.internet import task

R_Enc = Encoder.Encoder(19,26)
L_Enc = Encoder.Encoder(6,13)
IMU1 = IMU.IMU()

outputFile = open('simul-results.txt', 'w+')

def sample():
    time0 = time.time()
    sample = IMU1.sample()
    time1 = time.time()
    R_sample = R_Enc.sample()
    time2 = time.time()
    L_sample = L_Enc.sample()
    time3 = time.time()
    outputFile.write("%f\t%f\t%f\t%f\n\n" %(time0, time1, time2, time3))




if __name__ == "__main__":


    l = task.LoopingCall(sample)
    l.start(0.02)

    while True:
        
        time0 = time.time()
        sample = IMU1.sample()
        time1 = time.time()
        R_sample = R_Enc.sample()
        time2 = time.time()
        L_sample = L_Enc.sample()
        time3 = time.time()
        outputFile.write("%f\t%f\t%f\t%f\n\n" %(time0, time1, time2, time3))


    outputFile.close()
    
