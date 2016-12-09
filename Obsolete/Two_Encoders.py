import time
import RPi.GPIO as GPIO
import threading
from time import sleep


Enc1_A = 13
Enc1_B = 19
Enc2_A = 5
Enc2_B = 6

Rotary_counter = 0
Current_A = 1
Current_B = 1
PrevTime = time.time()
T =0
Velocity = 0

LockRotary = threading.Lock()      # create lock for rotary switch


# initialize interrupt handlers
def init():
   GPIO.setwarnings(False)
   GPIO.setmode(GPIO.BCM)               # Use BCM mode
                                 # define the Encoder switch inputs
   GPIO.setup(Enc_A, GPIO.IN)
   GPIO.setup(Enc_B, GPIO.IN)
                                 # setup callback thread for the A and B encoder
                                 # use interrupts for all inputs
   GPIO.add_event_detect(Enc_A, GPIO.RISING, callback=rotary_interrupt)             # NO bouncetime
   GPIO.add_event_detect(Enc_B, GPIO.RISING, callback=rotary_interrupt)             # NO bouncetime
   return



# Rotarty encoder interrupt:
# this one is called for both inputs from rotary switch (A and B)
def rotary_interrupt(A_or_B):
   global Rotary_counter, Current_A, Current_B, LockRotary, T, PrevTime, Velocity
                                       # read both of the switches
   Switch_A = GPIO.input(Enc_A)
   Switch_B = GPIO.input(Enc_B)
                                       # now check if state of A or B has changed
                                       # if not that means that bouncing caused it
   if Current_A == Switch_A and Current_B == Switch_B:      # Same interrupt as before (Bouncing)?
      return                              # ignore interrupt!

   Current_A = Switch_A                        # remember new state
   Current_B = Switch_B                        # for next bouncing check


   if (Switch_A and Switch_B):                  # Both ones active? Yes -> end of sequence
      LockRotary.acquire()                  # get lock

      T = time.time()-PrevTime
      if(T != 0):
         Velocity = 0.05 * 3.14159 / (400*T)
      else:
         Velocity = 0

      if A_or_B == Enc_B:                     # Turning direction depends on
         Rotary_counter += 1                  # which input gave last interrupt
      else:                              # so depending on direction either
         Rotary_counter -= 1                  # increase or decrease counter
         Velocity = Velocity * -1

      LockRotary.release()                  # and release lock
      PrevTime = time.time()
   return                                 # THAT'S IT

# Main loop. Demonstrate reading, direction and speed of turning left/rignt
def main():
   global Rotary_counter, LockRotary



   NewCounter = 0                        # for faster reading with locks


   init()                              # Init interrupts, GPIO, ...

   while True :                        # start test
      sleep(0.1)                        # sleep 100 msec

                                    # because of threading make sure no thread
                                    # changes value until we get them
                                    # and reset them

      PrevTime = time.time();
      LockRotary.acquire()

      NewCounter = Rotary_counter
      V = Velocity

      LockRotary.release()


      print ("Position = " + str(NewCounter*360/400) , "Velocity = " + str(V))



# start main demo function
main()
