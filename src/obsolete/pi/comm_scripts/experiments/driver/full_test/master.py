import serial

from core.network import Network


def main():
    # Create a serial port with which to communicate with an Arduino
    ser = serial.Serial(
        port='/dev/ttyACM0',
        baudrate=9600,
    )
    # Create a `Network` that can read in packets that are less than
    # or equal to 1024 bytes, and that stores the last 10 messages
    # it received.
    network = Network(1024, 10)
    try:
        while True:
            # noinspection PyBroadException
            try:
                # Decode the info coming from the Arduino
                command = ser.readline().decode('utf-8')
                # Broadcast the command to any Raspberry Pi's that are
                # listening.
                network.broadcast("<command>" + command + "</command>")
            except Exception:
                pass
    except KeyboardInterrupt:
        network.close_broadcast()


if __name__ == "__main__":
    main()