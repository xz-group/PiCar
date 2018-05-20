import time

from core.network import Network


def main():
    """A simple test to calculate the round trip time of
    packets

    This test was performed on: 3/21/2018
    Results: Overwhelmingly successful. See a fuller description
    on the log page:
    (https://classes.engineering.wustl.edu/ese205/core/index.php?title=Pi_Car_Comm_Log#Timing_Test_.28Finally.29)

    :return: None
    """
    network = Network(1024, 10)
    while True:
        message = "<token>Token data</token>"               # send token data every 2 seconds
        network.broadcast(message)
        time.sleep(2)


if __name__ == "__main__":
    main()
