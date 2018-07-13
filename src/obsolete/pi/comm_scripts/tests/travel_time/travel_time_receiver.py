import socket
import datetime

from core.network import Network


def main():
    """A receiver module for the travel_time test. This module will
    receive packets and compare their timestamp to the current
    time to see how long they spent in transit. It will write these
    data to an output file for viewing.
    :return: None

    """
    network = Network(1024, 10)
    network.start_listening(socket.SOCK_DGRAM)
    out_file = open("timing_output.log", "w")
    start = datetime.datetime.now()
    while (datetime.datetime.now() - start) < datetime.timedelta(seconds=30):
        try:
            unreads = network.read(network.buffer_size)                         # read out all unread messages
            for unread in unreads:
                # noinspection PyBroadException
                try:
                    str_time_sent = unread.find_values("s")[0].split("_")       # read in the timestamp
                    time_sent = datetime.datetime(
                        year        =   int(str_time_sent[0]),
                        month       =   int(str_time_sent[1]),
                        day         =   int(str_time_sent[2]),
                        hour        =   int(str_time_sent[3]),
                        minute      =   int(str_time_sent[4]),
                        second      =   int(str_time_sent[5]),
                        microsecond =   int(str_time_sent[6])
                    )
                    current_time = datetime.datetime.now()
                    delta_time = (current_time - time_sent).total_seconds()     # compare timestamp with current time
                    out_file.write(                                             # log the incoming message to a file
                        "Received message: "
                        + unread.content
                        + "At time: "
                        + str(current_time)
                        + ". The time of flight was: "
                        + str(delta_time)
                        + " seconds"
                        + "\n"
                    )
                except Exception:                                               # Ignore corrupted messages
                    continue
        except KeyboardInterrupt:               # Allow the user to stop execution with the keyboard.
            network.stop_listening()
            out_file.close()
    network.stop_listening()
    out_file.close()


if __name__ == "__main__":
    main()
