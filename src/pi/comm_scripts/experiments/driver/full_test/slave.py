import serial
import socket
import time
import datetime

from core.network import Network


def main():
    # Open a serial port to give the Arduino commands
    ser = serial.Serial(
        port="/dev/ttyACM0",
        baudrate=9600,
    )
    start = datetime.datetime.now()
    # Create a network that can read in packets of length 1024 bytes or less
    # and that stores the last 10 messages ir received.
    network = Network(1024, 10)
    # Start listening for messages (UDP packets).
    network.start_listening(socket.SOCK_DGRAM)
    try:
        while True:
            time = datetime.datetime.now() - start
            incoming_message = network.read(network.buffer_size)
            for message in incoming_message:
                try:
                    print("Message from: " + message.find_values("f"))
                    print("Steering: " + message.find_values("command").split(".")[1])
                    print("Throttle: " + message.find_values("command").split(".")[0])
                    print("Time since startup: " + str(time))
                except Exception:
                    pass
            """incoming_command = network.read(network.buffer_size)
            if len(incoming_command) > 0:
                incoming_command = incoming_command[0].find_values("command")
                if len(incoming_command) > 0:
                    tmp = incoming_command[0].split(".")
                    esc = tmp[0].strip()
                    steer = tmp[1].strip()
                    ser.write(("e" + esc + "s" + steer).encode('utf-8'))
                    time.sleep(0.01)"""
    except KeyboardInterrupt:
        network.stop_listening()


if __name__ == "__main__":
    main()
