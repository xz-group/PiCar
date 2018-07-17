from contrib.outgoing_message import OutgoingMessage
from contrib.incoming_message import IncomingMessage


def main():
    content = "<v>[10,10,0]</v><p>[10.3, 5, 0]</p>"
    outgoing = OutgoingMessage("255.255.255.255", "192.168.1.2", content)
    print("Outgoing message: " + str(outgoing))
    incoming = IncomingMessage(outgoing.content)
    print("Incoming message: " + str(incoming))
    print("Incoming message was broadcast: " + str(incoming.was_broadcast))
    print("Incoming message was sent to: " + str(incoming.find_values("t")))
    print("Incoming message was sent from: " + str(incoming.find_values("f")))
    print("Incoming message was sent at time: " + str(incoming.find_values("ts")))



if __name__ == "__main__":
    main()