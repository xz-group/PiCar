import serial
import time


def main():
    ser = serial.Serial(
        port='/dev/ttyACM0',
        baudrate=9600,
    )
    while True:
        ser.write('e1500s1500'.encode('utf-8'))
        time.sleep(10)
        ser.write('e1700s1700'.encode('utf-8'))
        time.sleep(10)


if __name__ == "__main__":
    main()
