import sys

from tests.travel_time import travel_time_receiver, travel_time_sender
from experiments.driver import driver, reader
from experiments.driver.full_test import master, slave


def main():
    """
    Testing method for various methods and functions
    :return: none
    """
    if len(sys.argv) == 1 or len(sys.argv) > 2:
        print_instructions()
    elif len(sys.argv) == 2:
        if sys.argv[1] == "test":
            while True:
                test_type = input("What kind of test would you like to run ('timing', 'driving', 'read', 'full')?\n")
                if test_type == "timing":
                    while True:
                        role = input("Is this machine a sender or receiver (s/r)?\n")
                        if role.startswith("s") or role.startswith("S"):
                            print("Running the sender's script... (CTRL-BREAK to halt)")
                            travel_time_sender.main()
                            break
                        elif role.startswith("r") or role.startswith("R"):
                            print("Running the receiver's script... (CTRL-BREAK to halt)")
                            travel_time_receiver.main()
                            break
                        else:
                            print("I could not parse that input, " + str(role) + "\nPlease try again.")
                    break
                elif test_type == "driving":
                    driver.main()
                elif test_type == "read":
                    reader.main()
                elif test_type == "full":
                    while True:
                        role = input("Is this machine the master or slave?\n")
                        if role.startswith("m"):
                            master.main()
                            break
                        elif role.startswith("s"):
                            slave.main()
                            break
                        else:
                            print("I could not parse that input")
                else:
                    print("That isn't a test I can run")
        elif sys.argv[1] == "master":
            master.main()
        elif sys.argv[1] == "slave":
            slave.main()
        else:
            print_instructions()
            sys.exit(1)


def print_instructions():
    print("Usage:\npython manage.py <action>")
    print("Action can be one of the following:")
    print("test\tRun a test of the network (for example, a timing test)")


if __name__ == "__main__":
    main()
