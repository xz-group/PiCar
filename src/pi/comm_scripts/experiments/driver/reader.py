import serial


def main():
    ser = serial.Serial(port='/dev/ttyACM0', baudrate=9600)
    while True:
        print(ser.readline().decode('utf-8'))


if __name__ == "__main__":
    main()
