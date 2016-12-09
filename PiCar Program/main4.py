import IMU, Encoder
import sys, socket, struct, time
from twisted.internet.protocol import Protocol, Factory, ClientFactory
from twisted.protocols.basic import LineOnlyReceiver
from twisted.internet import task, reactor
from twisted.web.server import Site
from twisted.web.resource import Resource
from ast import literal_eval

R_Enc = Encoder.Encoder(19, 26)
L_Enc = Encoder.Encoder(6, 13)
IMU1 = IMU.IMU()

payload = ['dummy']*4

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

def encRSample():
    timePre = time.time()
    sample = R_Enc.sample()
    payload[0] = sample
    timePost = time.time()
    outputFileEncR.write("%s\t%f\t%f\n" % (sample, timePre, timePost))

def encLSample():
    timePre = time.time()
    sample = L_Enc.sample()
    payload[1] = sample
    timePost = time.time()
    outputFileEncL.write("%s\t%f\t%f\n" % (sample, timePre, timePost))

def imuSample():
    timePre = time.time()
    sample = IMU1.sample()
    payload[2] = sample
    timePost = time.time()
    outputFileIMU.write("%s\t%f\t%f\n" % (sample, timePre, timePost))

def motiveSample():
    timePre = time.time()
    buffer = dataFactory.dataBuff
    length = len(buffer)
    if buffer is not None and length > 0:
        data = buffer[0]
        sample = [data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7]]
        payload[3] = sample
        print ('Motive:%s\n\n') % sample
        timePost = time.time()
        outputFileMotive.write('%s\t%f\t%f\n' % (sample, timePre, timePost))

class SocketClientProtocol(LineOnlyReceiver):
    # after framing is removed:
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

class WebPage(Resource):
    isLeaf = True

    def __init__(self):
        # self.inputHandle = inputHandle
        # self.payload = ["dummy"]*4
        pass

    def render_GET(self, request):
        return "<html><head><meta http-equiv= 'refresh' content='0.1'></head>" \
               "<body>" \
               "Right Encoder: %s""<br>""Left Encoder: %s""<br>""IMU: %s""<br>""Motive: %s" \
               "</body>" \
               "</html>" % (payload[0], payload[1], payload[2], payload[3])

    # def load(self):
    #     # TODO: define order for payload list
    #     if self.inputHandle is not None:
    #         # counter = 0
    #         # for client, line in self.inputHandle.client.iteritems():
    #         #     if line is not None:
    #         #         self.payload[counter] = line
    #         #     counter += 1
    #         if (line = self.inputHandle.frame) is not None:
    #             payload[0] = line
    #
    #     else:
    #         print("no data available from motive")

if __name__ == "__main__":

    # benchmarks:
    outputFileIMU = open('imu-simul-results.txt', 'w+')
    outputFileEncR = open('encR-simul-results.txt', 'w+')
    outputFileEncL = open('encL-simul-results.txt', 'w+')
    outputFileMotive = open('motive-simul-results.txt', 'w+')

    host = findHost()
    dataFactory = SocketClientFactory()

    if (host is not None):
        print ('Attempting connection to %s:%s') % (host, defaultTwistedServerPort)
        reactor.connectTCP(host, defaultTwistedServerPort, dataFactory)
        l_motive = task.LoopingCall(motiveSample)
        l_motive.start(0.02)
    else:
        print ('could not find Motive server host')

    l_imu = task.LoopingCall(imuSample)
    l_encr = task.LoopingCall(encRSample)
    l_encl = task.LoopingCall(encLSample)
    l_imu.start(0.02)
    l_encr.start(0.02)
    l_encl.start(0.02)

    resource = WebPage()
    webFactory = Site(resource)
    reactor.listenTCP(8881, webFactory)

    reactor.run()

    outputFileIMU.close()
    outputFileEncR.close()
    outputFileEncL.close()
    outputFileMotive.close()



