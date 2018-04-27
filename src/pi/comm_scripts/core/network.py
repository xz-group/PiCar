import socket
import multiprocessing
import os
import time
import signal
import queue as Queue

from contrib.incoming_message import IncomingMessage
from contrib.outgoing_message import OutgoingMessage
from helpers.helpers import get_config, get_ip


def main():
    """ A simple processing example that concurrently runs two delay timed
    loops that print out information about the process they're running on.
    Used to allow the network to listen while it sends out information.
    
    """
    processes = list()
    processes.append(multiprocessing.Process(name="thread1", target=target, args=(1, 2)))
    processes.append(multiprocessing.Process(name="thread2", target=target, args=(2, 3)))
    print("Parent process id: " + str(os.getpid()))
    for process in processes:
        process.start()


def target(num1, num2):
    """

    :param num1:
    :param num2:
    :return: none
    """
    for i in range(4):
        print("Executing target: " + str(num1) + " with process: " + str(os.getpid()) +
              "\nWhose parent process is: " + str(os.getppid()))
        time.sleep(num2)
    os.abort()


class Network:
    def __init__(self, max_packet_length, buffer_size):
        """

        :param max_packet_length:
        :param buffer_size:
        :return: None
        """
        config_dict = get_config("network.conf")
        self.signature = get_ip()
        if self.signature is None:
            raise RuntimeError("Could not get ip address")
        try:
            self.port = int(config_dict['port'])
        except KeyError:
            raise RuntimeError("Key 'port' not in config file")
        except ValueError:
            raise RuntimeError("'port' could not be read as an int")
        self.max_packet_length = max_packet_length

        self.logged_messages = []
        self.buffer_size = buffer_size
        self.listening_process = None

        self.broadcast_socket = None
        self.listen_socket = None
        self.queue = multiprocessing.Queue(maxsize=self.buffer_size)
        self.timeout = 0.01                                     # Timeout for Queue requests in seconds
        
    def start_listening(self, connection_type):
        """
        Command to start listening for incoming messages of a specified type
        :param connection_type: a constant that's specified in the constant library
            example:
                socket.SOCK_DGRAM   - specifies a udp socket
                socket.SOCK_STREAM  - specifies a tcp socket
        :return: None

        """
        if self.listen_socket is None:
            try:
                self.listen_socket = socket.socket(socket.AF_INET, connection_type)
                self.listen_socket.bind(("255.255.255.255", self.port))     # Listen for packet from any port
                self.listening_process = multiprocessing.Process(
                    name="listening_process_"+str(self.signature)+"d",
                    target=self.update_messages,
                    args=(self.queue,))
                self.listening_process.daemon = True
                self.listening_process.start()
            except RuntimeError:
                raise RuntimeError("Listening socket failed to open")
        
    def stop_listening(self):
        """
        Command to stop listening for incoming messages
        :return: None

        """
        # noinspection PyBroadException
        try:
            os.kill(self.listening_process.pid, signal.CTRL_C_EVENT)
        except Exception:
            os.kill(self.listening_process.pid, signal.SIGTERM)
        self.listen_socket = None

    def update_messages(self, queue):
        """
        Update the queue to include the latest message
        :param queue: A multiprocessing.Queue object that is shared between this and its parent process
        :return: None
        """
        while True:
            data, addr = self.listen_socket.recvfrom(self.max_packet_length)
            incoming_message = IncomingMessage(data.decode("utf-8"))            # Convert bytes to string
            if self.signature != str(addr):                                     # if the message isn't from us
                try:
                    queue.put(incoming_message, False)                              # Add message to queue, don't block
                    print(incoming_message)
                except Queue.Full:
                    pass
        
    def broadcast(self, message):
        """Sends an outgoing message to the IP address 255.255.255.255
        :param message: The message that is being broadcasted
        :return: None

        """
        if self.broadcast_socket is None:
            self.broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        broadcast_addr = "255.255.255.255"
        outgoing_message = OutgoingMessage(broadcast_addr, self.signature, message)
        self.broadcast_socket.sendto(outgoing_message.content.encode('utf-8'),
                                     (broadcast_addr, self.port))
        print(outgoing_message)

    def close_broadcast(self):
        """Stops broadcasting messages and closing the broadcasting socket
        :return: None

        """
        try:
            self.broadcast_socket.shutdown()                             # stops broadcasting
            self.broadcast_socket.close()                                # closes the broadcasting socket
        except Exception:                                                # checks for an exception
            raise RuntimeWarning("Could not close broadcast_socket")
        self.broadcast_socket = None

    def read(self, num_msgs=1):
        """Return a list containing the first `num_msgs` messages from unreads
        and move them to `self.logged_messages` (moving the oldest messages out of
        logged_messages)
        :param num_msgs: an integer representing the number of messages to read
        :return: list<Message> containing the oldest unread messages, None if num_msgs is not an int

        """
        try:
            num_msgs = int(num_msgs)
            if num_msgs > self.buffer_size:
                num_msgs = self.buffer_size
        except ValueError:
            return None
        r = []
        for i in range(num_msgs):
            try:
                r.append(self.queue.get(False))             # Extract from the queue without blocking
            except Queue.Empty:                             # pass if queue is empty
                pass
        tmp = r[:]
        tmp.extend(self.logged_messages[:self.buffer_size-len(r)][:])       # Put messages in logged_messages
        self.logged_messages = tmp
        return r


if __name__ == "__main__":
    main()
