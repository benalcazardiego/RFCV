from twisted.internet import reactor, protocol
import sys

class Echo(protocol.Protocol):
    
    def dataReceived(self, data):
        """ Echo everything """
        self.transport.write(data)
        print data


def main(port):
    """This runs the protocol on port 1225"""
    factory = protocol.ServerFactory()
    factory.protocol = Echo
    reactor.listenTCP(port,factory)
    reactor.run()

# this only runs if the module was *not* imported
if __name__ == '__main__':
    port = sys.argv[1]
    main(int(port))
