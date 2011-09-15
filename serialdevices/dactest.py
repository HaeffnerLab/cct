from serialdeviceserver import SerialDeviceServer, setting, inlineCallbacks, SerialDeviceError, SerialConnectionError, PortRegError
from labrad.types import Error
from twisted.internet import reactor
from twisted.internet.defer import returnValue
import binascii

TIMEOUT = 1.0
RESP_STRING = 'r'

class DacTest(SerialDeviceServer):
    
    serialstr = '/dev/tty.usbserial-FTFA67XY'
    
    @inlineCallbacks
    def initServer( self ):
        serStr = yield self.findSerial( 'cctmain' )
        self.initSerial( serStr, self.serialstr )

    def makeComString(self, numPortsChanged, portNum, setNum, codeInDec ):

        """
        Pass the voltage code in decimal
        Form the string to communicate with the DAC
        """
        
        nChanged = binascii.unhexlify(hex(numPortsChanged)[2:].zfill(4)) # Number of ports to change
        port =  binascii.unhexlify(hex(portNum)[2:].zfill(4)) # Which port to change
        set = binascii.unhexlify(hex(setNum)[2:].zfill(4)) # Which set of updates are we applying
        code = binascii.unhexlify(hex(int(codeInDec))[2:].zfill(4)) # What digital code to write to the port
        
        comstr = nChanged + port + set + code
        return comstr

    @setting(10, "Write Code", code='v')
    def writeACode( self, c, code):
        comstr = self.makeComString( 1, 7, 0, code )
        wr = yield self.ser.write(comstr)
        resp = yield self.ser.read( len( RESP_STRING ) )
        print len(resp)
    
if __name__ == "__main__":
    from labrad import util
    util.runServer(DacTest())
