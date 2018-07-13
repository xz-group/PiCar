from contrib.message import Message


def main():
    """A simple unit test of the `IncomingMessage` class.
    :return: None
    """
    my_incoming_message = IncomingMessage("<t>192.168.1.2</t>"
                                          "<f>192.168.1.3</f>"
                                          "<s>2018_2_18_0_0_0_0</s>")
    print("Incoming message: " + str(my_incoming_message))
    print("Was broadcast: " + str(my_incoming_message.was_broadcast))

    my_incoming_message = IncomingMessage("<f>192.168.1.3</f>"
                                          "<s>2018_2_18_0_0_0_0</s>")
    print("Incoming message: " + str(my_incoming_message))
    print("Was broadcast: " + str(my_incoming_message.was_broadcast))

    my_incoming_message = IncomingMessage("<t>255.255.255.255</to>"
                                          "<f>192.168.1.3</f>"
                                          "<s>2018_2_18_0_0_0_0</s>")
    print("Incoming message: " + str(my_incoming_message))
    print("Was broadcast: " + str(my_incoming_message.was_broadcast))


class IncomingMessage(Message):
    def __init__(self, content):
        super().__init__(content)
        self.was_broadcast = self.was_broadcast()

    def was_broadcast(self):
        """A method to determine whether or not the this message was broadcast
        :return: A boolean representing whether the message was broadcast
        """
        return len(self.find_values("t")) == 0 or self.find_values("t")[0][0:3] == "255"

    def directed_at_addr(self, addr):
        """A method to determine if the message was directed at the target `addr`
        :param addr: The target address to check
        :return: A boolean representing whether the message was targeted at `addr`
        """
        return self.find_values("t")[0] == addr


if __name__ == "__main__":
    main()
