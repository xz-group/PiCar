from ctypes import *
path = "LSM9DS1_RaspberryPi_Library/lib/counter.so"
counter = cdll.LoadLibrary(path)

counter.ccnt_read.argtypes = []
counter.ccnt_read.restype = c_int

