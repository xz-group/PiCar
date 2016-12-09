import sys, socket, struct, time
from twisted.internet.protocol import Protocol, Factory, ClientFactory
from twisted.protocols.basic import LineOnlyReceiver
from twisted.internet import task, reactor
from ast import literal_eval

hostName = 'bach.ese.wustl.edu'
host = None
defaultTwistedServerPort = 53335

# use win32 reactor if applicable
if sys.platform == 'win32':
    from twisted.internet import win32eventreactor
    win32eventreactor.install()

# find hostname
def findHost():
    addr = socket.gethostbyname(hostName)
    return addr


class SocketClientProtocol(LineOnlyReceiver):
    # after int prefix and other framing are removed:
    def lineReceived(self, line):
        self.factory.got_msg(line)

    def connectionMade(self):
        self.transport.setTcpNoDelay(True)
        print ("connected to twisted server")
        self.factory.clientReady(self)


class SocketClientFactory(ClientFactory):
    """ Created with callbacks for connection and receiving.
        send_msg can be used to send messages when connected.
    """
    protocol = SocketClientProtocol

    def __init__(self):
        self.client = None
        self.dataBuff = []

    def clientConnectionFailed(self, connector, reason):
        print ("connection failed because of %s"), reason
        outputFileMotive.close()
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        print ("connection lost due to: %s"), reason
        outputFileMotive.close()
        reactor.stop()

    def clientReady(self, client):
        self.client = client

    def got_msg(self, msg):
        # data = literal_eval(msg)
        data = literal_eval(str(map(str,msg.split(','))))

        if self.dataBuff:
            self.dataBuff[0] = data

        else:
            self.dataBuff.append(data)

        # for payload in self.dataBuff:
        #     outputFileMotive.write(payload)
        # outputFileMotive.write('\tTime Interval: %f\tRunning Time: %f\n' %(timeInterval, accumTime))

def motiveSample():
    timePre = time.time()
    buffer = dataFactory.dataBuff
    length = len(buffer)
    if buffer is not None and length > 0:
        data = buffer[0]
        sample = [data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7]]
        print ('sample is %s\n', sample)
        timePost = time.time()
        outputFileMotive.write('%s\t%f\t%f\n' % (sample, timePre, timePost))

if __name__ == "__main__":
    host = findHost()
    dataFactory = SocketClientFactory()

    outputFileMotive = open('motive-simul-results.txt', 'w+')

    if (host is not None):
        print ('Attempting connection to %s:%s') % (host, defaultTwistedServerPort)
        reactor.connectTCP(host, defaultTwistedServerPort, dataFactory)
        l_motive = task.LoopingCall(motiveSample)
        l_motive.start(0.02)

    else:
        print ("could not find host")

    reactor.run()

    outputFileMotive.close()


