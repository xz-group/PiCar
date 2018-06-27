from Motor import Motor
from Encoder import Encoder
import PID



class SpeedController (object):

    motor = 0
    encoder = 0
    speed = 0
    pid=0

    def __init__(self, motor, encoder, speed):

        self.motor = motor
        self.encoder = encoder
        self.speed = speed

        self.pid = PID.PID(10,0,0)
        self.pid.setSampleTime(0.02)

    def setSpeed(self, speed):
        self.speed = speed
        self.pid.SetPoint = speed

        position,velocity = self.encoder.sample()
        self.pid.update(velocity)

        out = self.pid.output
        self.motor.setSpeed(self.motor.speed+out)
       
