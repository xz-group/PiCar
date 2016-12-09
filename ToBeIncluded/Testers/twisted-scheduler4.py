"""
This version imports encoder and IMU class objects directly in-file and samples them on request
"""

from twisted.internet.protocol import Protocol, Factory, ClientFactory
from twisted.protocols.basic import LineOnlyReceiver
from twisted.internet import task
from twisted.web.server import Site
from twisted.web.resource import Resource
import sys, socket, struct, time
import IMU, Encoder

from twisted.internet import reactor

# timing benchmarks
prevTime = 0.0
accumTime = 0.0

motiveHostName = 'bach.ese.wustl.edu'
# sensorHost = '172.27.55.99'
# sensorHost = '172.27.55.204'

# Port assignments
defaultTwistedServerPort = 53335
#defaultEncoderPort1 = 50001
#defaultEncoderPort2 = 50002
#defaultIMUPort = 50003

R_Enc = Encoder.Encoder(19,26)
L_Enc = Encoder.Encoder(6,13)
IMU1 = IMU.IMU()

payload = ["dummy"]*4

def sample(resource):
    time0 = time.time()
    R_sample = R_Enc.sample()
    payload[1] = R_sample
    time1 = time.time()

    L_sample = L_Enc.sample()
    payload[2] = L_sample

    time2 = time.time()
    IMU1.setIMUVelocity(R_sample,L_sample) #Input Encoder velocity to fix reset IMU velocity

    sample = IMU1.sample()
    payload[3] = sample

    time3 = time.time()
    resource.load()

    time4 = time.time()

    outputFile.write("%f\t%f\t%f\t%f\t%f\n\n" %(time0, time1, time2, time3, time4))

# use win32 reactor if applicable
if sys.platform == 'win32':
    from twisted.internet import win32eventreactor
    win32eventreactor.install()

# find hostname
def findHost():
    addr = socket.gethostbyname(motiveHostName)
    return addr

############################################
class DataPage(Resource):
    isLeaf = True

    def __init__(self, inputHandle):
        self.inputHandle = inputHandle
        # self.payload = ["dummy"]*4

    def render_GET(self, request):
        return "<html><head><meta http-equiv= 'refresh' content='1'></head>" \
               "<body>" \
               "Data 1: %s""<br>""Data 2: %s""<br>""Data 3: %s""<br>""Data 4: %s" \
               "</body>" \
               "</html>" % (payload[0], payload[1], payload[2], payload[3])

    def load(self):
        # TODO: define order for payload list
        if self.inputHandle is not None:
            # counter = 0
            # for client, line in self.inputHandle.client.iteritems():
            #     if line is not None:
            #         self.payload[counter] = line
            #     counter += 1
            if (line = self.inputHandle.frame) is not None:
                payload[0] = line

        else:
            print("no data available from motive")


class SocketClientProtocol(LineOnlyReceiver):
    #def __init__(self):
        # self.delimiter = '\n'

    # after int prefix and other framing are removed:
    def lineReceived(self, line):
        self.factory.gotMsg(line, self)

    def connectionMade(self):   # calls when connection is made with Twisted server
        print ("connected to server")
        self.factory.clientReady(self)


class SocketClientFactory(ClientFactory):
    """ Created with callbacks for connection and receiving.
        send_msg can be used to send messages when connected.
    """
    protocol = SocketClientProtocol

    def __init__(self):
        # store references to client connections
        self.client = None
        self.frame = None

    def clientConnectionFailed(self, connector, reason):
        print ("connection failed due to: %s"), reason
        if self.client is None:
            outputFile.close()
            reactor.stop()

    def clientConnectionLost(self, connector, reason):
        print ("connection lost due to: %s"), reason
        if self.client is None:
            outputFile.close()
            reactor.stop()

    def clientReady(self, client):
        self.client = client

    def gotMsg(self, msg, client):
        #print (msg)
        # outputFile.write(msg)
        # outputFile.write('\n')
        global prevTime, accumTime

        currTime = time.time()
        timeInterval = currTime - prevTime

        if prevTime > 0.0:
            accumTime += timeInterval
        outputFile_motive.write(msg)
        outputFile_motive.write('\tTime Interval: %f\tRunning Time: %f\n' %(timeInterval, accumTime))
        self.frame = msg

###########################################

if __name__ == '__main__':

    outputFile = open('scheduler4-results.txt', 'w+')
    outputFile_motive = open('scheduler4-motive-results.txt', 'w+')

    dataFactory = SocketClientFactory()

    # Motive connections (dependent on MoCap PC)
    motiveHost = findHost()
    if motiveHost is not None:
        print ('Attempting connection to %s:%s') %(motiveHost, defaultTwistedServerPort)
        try:
            reactor.connectTCP(motiveHost, defaultTwistedServerPort, dataFactory)
        except:
            print ("Motive connection failed ... continuing with sensor connections")
    else:
        print ("could not find host")

    # Web server
    resource = DataPage(dataFactory)
    webFactory = Site(resource)
    reactor.listenTCP(8880, webFactory)

    l2 = task.LoopingCall(sample(resource))
    l2.start(0.020)

    reactor.run()
