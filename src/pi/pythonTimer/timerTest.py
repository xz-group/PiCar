from threading import Timer
import time
import csv

start = time.time()
last = time.time()
timeDiffer = []
filename = 'timer_accuracy.csv'
#50Hz = 0.02s
frequency = 0.01 
taskDuration = 10


def hello():
    global start,last
    #print("hello, world")
    #print("Time elapsed: %f" % (time.time() - last))
    timeDiffer.append(time.time() - last);
    last = time.time()
    if(time.time() - start < taskDuration):
        Timer(frequency, hello).start()
    else:
        print("start writing")
        with open(filename,"a",newline = '') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            for i in range(len(timeDiffer)):
                row = [timeDiffer[i]]
                spamwriter.writerow(row)
    

Timer(0.02,hello).start()
