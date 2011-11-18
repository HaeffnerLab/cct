'''
9 Aug 2011
Dylan Gorman

Adapted from laserdacbox.py
'''

from serialdeviceserver import SerialDeviceServer, setting, inlineCallbacks, SerialDeviceError, SerialConnectionError, PortRegError
from twisted.internet import reactor
from twisted.internet.defer import returnValue
import binascii
from labrad.server import Signal
import copy as cpy # copy objects by value
from numpy import *
import sys
import os

SERVERNAME = 'CCTDAC'
PREC_BITS = 16.
DAC_MAX = 2500.
MAX_QUEUE_SIZE = 1000
#time to wait for response from dc box
TIMEOUT = 0.01
#expected response from dc box after write
RESP_STRING = 'r'
#time to wait if correct response not received
ERROR_TIME = 1.0
SIGNALID = 270837

NUMCHANNELS = 18

# Nominal analog voltage range. Just used if there's no calibration available
NOMINAL_VMIN = -10.0
NOMINAL_VMAX = 10.0

class DCBoxError( SerialConnectionError ):
    errorDict = {
        0:'Invalid channel name',
        1:'Voltage out of range',
        2:'Queue size exceeded',
        3:'Shutter input must be boolean',
        4:'Must set value before you can retrieve',
        5:'Correct response from DC box not received, sleeping for short period'
        }

class Port():
    """
    Store information about ports
    """
    def __init__(self, portNumber):
        self.portNumber = portNumber
        self.analogVoltage = None
        self.digitalVoltage = None
    
        """
        Try to get calibration from registry. If no calibration exists, use the naive value.
        We will obtain, in either case, a function of the form
        
        analog voltage = m*(digital voltage) + b
        """

        #registry.cd(['Calibrations'])
        #(subs, keys) = registry.dir()
        
        #if str(portNumber) in subs:
        #    registry.cd(['', 'Calibrations', str(portNumber)])
        #    self.m = registry.get('slope')
        #    self.b = registry.get('y_int')

        #else:
        self.m = (NOMINAL_VMAX - NOMINAL_VMIN)/float((2**PREC_BITS - 1)) # slope
        self.b = NOMINAL_VMIN #intercept
    
    def setAnalogVoltage(self, av):
        """
        Assume, for the moment, that the calibration is linear in the form:
        av = m*(digital code) + b
        
        so that digital code = ( (analog voltage) - b ) / m
        """

        self.analogVoltage = float(av)
        dv = int(round( (av - self.b) / float(self.m) ))
        
        if dv < 0:
            self.digitalVoltage = 0 # Set to the minimum acceptable code
        elif dv > ( 2**PREC_BITS - 1 ): # Largest acceptable code
            self.digitalVoltage = (2**PREC_BITS - 1)
        else:
            self.digitalVoltage = dv

    def setDigitalVoltage(self, dv):
        if dv < 0:
            self.digitalVoltage = 0
            self.analogVoltage = self.b
        elif dv > ( 2**PREC_BITS - 1 ):
            self.digitalVoltage = (2**PREC_BITS - 1)
            self.analogVoltage = self.m*(2**PREC_BITS - 1) + self.b
        else:
            self.digitalVoltage = dv
            self.analogVoltage = self.m*dv + self.b
        
        
class CCTDACServer( SerialDeviceServer ):
    """
    CCTDAC Server
    Used for controlling DC trap electrodes

    portList always holds the _most recent_ values. If a list cannot be written
    because the serial port is unavailable, the portList is copied (by value!) to
    the queue, and the portList can be safely updated.
    """

    name = SERVERNAME
    regKey = 'CCTDac'
    port = None
    serNode = 'cctmain'
    timeout = TIMEOUT
    onNewUpdate = Signal(SIGNALID, 'signal: ports updated', 's')

    @inlineCallbacks
    def initServer( self ):
        """
        Initialize CCTDACServer
        """
        self.createInfo() # Populate list of Channels
        self.queue = []
        if not self.regKey or not self.serNode: raise SerialDeviceError( 'Must define regKey and serNode attributes' )
        port = yield self.getPortFromReg( self.regKey )
        self.port = port
        try:
            print self.serNode
            serStr = yield self.findSerial( self.serNode )
            #self.initSerial( serStr, port, baudrate=56000 )
            self.initSerial( serStr, port)
        except SerialConnectionError, e:
            print "SERIAL CONNECTION ERROR"
            self.ser = None
            if e.code == 0:
                print 'Could not find serial server for node: %s' % self.serNode
                print 'Please start correct serial server'
            elif e.code == 1:
                print 'Error opening serial connection'
                print 'Check set up and restart serial server'
            else: raise
        self.listeners = set()
        self.free = True

    def createInfo( self ):
        """
        Initialize channel list
        """
        self.portList = []
        for i in range(1, NUMCHANNELS + 1): # Port nums are indexed from 1 in the microcrontroller (I think)
            #self.portList.append(Port(i, self.client.registry))
            self.portList.append(Port(i))

    @inlineCallbacks
    def checkQueue( self, c ):
        """
        When timer expires, check queue for values to write
        """
        if self.queue:
            print 'clearing queue...(%d items)' % len( self.queue )
            yield self.writeToSerial(c, self.queue.pop( 0 ) )
        else:
            print 'queue free for writing'
            self.free = True

    @inlineCallbacks
    def tryToUpdate( self, c, ports ):
        """
        Check if serial connection is free.
        If free, write the list of ports to the DAC.
        If not free, store the port list in the queue.
        Raise error when queue fills up.
        
        @param channel: Channel to write to
        @param value: Value to write
        
        @raise DCBoxError: Error code 2.  Queue size exceeded
        """
        if self.free:
            self.free = False
            yield self.writeToSerial(c, ports )
        elif len( self.queue ) > MAX_QUEUE_SIZE:
            raise DCBoxError( 2 )
        else:
            newPorts = [ cpy.copy(p) for p in ports] # copy the portList by value into the queue
            self.queue.append( newPorts )
            

    @inlineCallbacks
    def writeToSerial( self, c, ports ):
        """
        Write value to specified channel through serial connection.
        
        Convert message to microcontroller's syntax.

        There's currently no confirmation from the DAC, so we assume everything's worked.
        We'll prob want to make the DAC confirm a successful update

        After the list has been written, update the current portList
        """
        self.checkConnection()
        toSend = self.makeComString( ports )
        #print binascii.hexlify(toSend)
        yield self.ser.write( toSend )
        #print 'about to read'
        #resp = yield self.ser.read( len( ports ) )
        #print 'read',resp, len(resp)
        #self.portList = [ cpy.copy(p) for p in ports ] # now that the new values have been written, update the portList
        for p in ports:
            self.portList[p.portNumber-1] = cpy.copy(p)
        self.notifyOtherListeners(c)
        yield self.checkQueue(c)

    def makeComString(self, ports):

            
        """
        Pass a list of Port objects to update. The updated value must already be written to the Port.

        Construct a com string in the appropriate format.
        """
        numPortsChanged = len(ports)
        setNum = 1
        
        nChanged = binascii.unhexlify(hex(numPortsChanged)[2:].zfill(2)) # Number of ports to change

        comstr = nChanged
        for p in ports:
            portNum = p.portNumber
            codeInDec = p.digitalVoltage
            # a hack to make the least significant bit a 0 to deal
            # with an obscure problem in the FPGA code.
            #if codeInDec % 2:
            #    codeInDec = codeInDec - 1
            #print codeInDec
            port =  binascii.unhexlify(hex(portNum)[2:].zfill(2)) # Which port to change
            setn = binascii.unhexlify(hex(setNum)[2:].zfill(4)) # Which set of updates are we applying ( = 1 for now, always)
            code = binascii.unhexlify(hex(codeInDec)[2:].zfill(4)) # What digital code to write to the port
            comstr += 'P' + port + 'I' + setn + ',' + code
        return comstr
    
    def initContext(self, c):
        self.listeners.add(c.ID)
    
    def expireContext(self, c):
        self.listeners.remove(c.ID)
    
    def notifyOtherListeners(self, context):
        """
        Notifies all listeners except the one in the given context
        """
        notified = self.listeners.copy()
        notified.remove(context.ID)
        self.onNewUpdate('Channels updated', notified)
        print "Notifyin' them listeners"
    
    @setting( 0 , 'Set Digital Voltages', returns = '' )
    def setDigitalVoltages( self, c, digitalVoltages ):
        """
        Pass digitalVoltages, a list of digital voltages to update.
        Currently, there must be one for each port.
        """
        newPorts = [ Port(i) for i in range(1, NUMCHANNELS + 1) ]
        for (p, dv) in zip(newPorts, digitalVoltages):
            p.setDigitalVoltage(dv)
        self.tryToUpdate(c, newPorts )
        

    @setting( 1 , 'Set Analog Voltages', analogVoltages='*v', returns = '' )
    def setAnalogVoltages( self, c, analogVoltages ):
        """
        Pass analogVoltages, a list of analog voltages to update.
        Currently, there must be one for each port.
        """ 
        newPorts = [ Port(i) for i in range(1, NUMCHANNELS + 1) ]
        for (p, av) in zip(newPorts, analogVoltages):
            p.setAnalogVoltage(av)
        yield self.tryToUpdate(c, newPorts )
 

    @setting( 2, 'Set Individual Analog Voltages', analogVoltages='*(iv)', returns = '')
    def setIndivAnaVoltages(self, c, analogVoltages ):
        """
        Pass a list of tuples of the form:
        (portNum, newVolts)
        """
        newPorts = []
        for (num, av) in analogVoltages:
            p = Port(num)
            p.setAnalogVoltage(av)
            newPorts.append(p)
        yield self.tryToUpdate(c, newPorts)

    @setting( 3, 'Get Analog Voltages', returns = '*v' )
    def getAnalogVoltages(self, c):
        """
        Return a list of the analog voltages currently in portList
        """
        return [ p.analogVoltage for p in self.portList ]  # Yay for list comprehensions

    @setting( 4, 'Get Digital Voltages' )
    def getDigitalVoltages(self, c):
        """
        Return a list of digital voltages currently in portList
        """
        
        return [ dv for v in [ p.digitalVoltage for p in self.portList ] ]
    
    @setting( 5, 'Set Multipole Control File', file='s: multipole control file')
    def setMultipoleControlFile(self, c, file):
        """
        Read in a matrix of multipole values
        """

        data = genfromtxt(file)
        self.multipoleVectors = {}
        self.multipoleVectors['Ex'] = data[:,0]
        self.multipoleVectors['Ey'] = data[:,1]
        self.multipoleVectors['Ez'] = data[:,2]
        self.multipoleVectors['U1'] = data[:,3]
        self.multipoleVectors['U2'] = data[:,4]
        self.multipoleVectors['U3'] = data[:,5]
        self.multipoleVectors['U4'] = data[:,6]
        self.multipoleVectors['U5'] = data[:,7]
        
    @setting( 6, 'Set Multipole Voltages', ms = '*(sv): dictionary of multipole voltages')
    def setMultipoleVoltages(self, c, ms):
        """
        set should be a dictionary with keys 'Ex', 'Ey', 'U1', etc.
        """
        
        multipoleSet = {}
        for (k,v) in ms:
            multipoleSet[k] = v
        
        self.multipoleSet = multipoleSet # may want to keep track of the current set.
        realVolts = zeros(NUMCHANNELS)
        for key in self.multipoleVectors.keys():
            #print self.multipoleVectors[key]
            realVolts += dot(multipoleSet[key],self.multipoleVectors[key])
            #realVolts += multipoleSet[key] * self.multipoleVectors[key]
        self.setAnalogVoltages(c, realVolts)
    
    @setting( 7, 'Get Multipole Voltages',returns='*(s,v)')
    def getMultipoleVolgates(self, c):
        print "Shhhh... I shouldn't be here!"
        return self.multipoleSet.items()
    
        
if __name__ == "__main__":
    from labrad import util
    util.runServer( CCTDACServer() )
