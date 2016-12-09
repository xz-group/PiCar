# uses netstring receiver as both the subclass for input and output

# !/usr/bin/env python

# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

from twisted.internet import defer, task
from twisted.internet.protocol import Protocol, ClientFactory, ServerFactory, Factory
from twisted.protocols import basic
import sys, time, struct

prevTime = 0.0
streamError = []

if sys.platform == 'win32':
    from twisted.internet import win32eventreactor
    win32eventreactor.install()

class OutputProtocol(object, basic.NetstringReceiver):
    def __init__(self):
        self.MAX_LENGTH = 33    # seven 4-byte values
        self.count = 0

    def connectionMade(self):
        self.transport.setTcpNoDelay(True)
        print ("Got a RPi connection!")
        self.transport.write("hello :-)!\r\n")
        self.factory.client_list.append(self)

    def connectionLost(self, reason):
        print "Lost client %s! Reason: %s\n" % (self, reason)
        self.factory.client_list.remove(self)

    def sendMsg(self, data):
        self.sendString(data)


class OutputProtocolFactory(ServerFactory):
    protocol = OutputProtocol

    def __init__(self):
        self.client_list = []

    def sendToAll(self, data):
        # check if dict is empty
        if self.client_list:
            for client in self.client_list:
                client.sendMsg(data)


class InputProtocol(basic.NetstringReceiver):
    def __init__(self, outputHandle):
        self.MAX_LENGTH = 33;
        self.dataBuff = []
        self.outputHandle = outputHandle
        print ("Input Protocol built")

    def connectionMade(self):
        self.transport.setTcpNoDelay(True)
        print ("Connected to Motive")

    def stringReceived(self, string):
        # global prevTime
        # currTime = time.clock()

        bytesReceived = sys.getsizeof(string)
        print 'Size of data: %d\n' % (bytesReceived)  # prints out 66 bytes... padding?

        # convert to binary format - this gets condensed down to 33 bytes
        # binData = ' '.join('{0:08b}'.format(ord(x), 'b') for x in string)
        # outputFile_bin.write(binData)
        # outputFile_bin.write('\tReceived %d bytes\tBefore: %f\tNow: %f\n\n' % (bytesReceived, prevTime, currTime))

        # try:
        #     self.dataBuff.append(struct.unpack("!HBBBfffffff", string))
        #     outputFile.write(str(self.dataBuff))
        # except:
        #     print 'Failed to unpack\n'

        # outputFile.write('\tBefore: %f\tNow: %f\n\n' % (prevTime, currTime))
        # prevTime = currTime
        #
        # self.outputHandle.sendToAll(self.dataBuff)
        # self.dataBuff = []

        self.outputHandle.sendToAll(string)


class InputProtocolFactory(ClientFactory):
    def __init__(self, outputHandle):
        self.outputHandle = outputHandle

    def startedConnecting(self, connector):
        print 'Started to connect.'

    def buildProtocol(self, addr):
        print 'Connected.'
        return InputProtocol(self.outputHandle)

    def clientConnectionLost(self, connector, reason):
        print 'Lost MotiveClient connection.  Reason:', reason
        reactor.stop()
        sys.exit()

    def clientConnectionFailed(self, connector, reason):
        print 'Connection failed. Reason:', reason
        reactor.stop()
        sys.exit()


if __name__ == '__main__':
    from twisted.internet import reactor

    outputFile_bin = open(r'Data Files/motive_results_bin.txt', 'w+')
    outputFile = open(r'Data Files/motive_results.txt', 'w+')

    out = OutputProtocolFactory()
    reactor.listenTCP(53335, out, interface="192.168.95.109")
    reactor.connectTCP("192.168.95.109", 27015, InputProtocolFactory(out))

    reactor.run()

