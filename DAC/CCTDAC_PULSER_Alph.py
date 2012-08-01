'''
### BEGIN NODE INFO
[info]
name = CCTDAC_PULSER
version = 1.0
description = 
instancename = CCTDAC_PULSER

[startup]
cmdline = %PYTHON% %FILE%
timeout = 20

[shutdown]
message = 987654321
timeout = 20

### END NODE INFO
'''

from labrad.server import LabradServer, setting, Signal, inlineCallbacks 
from twisted.internet import reactor
from twisted.internet.defer import returnValue
import copy as cpy # copy objects by value
from numpy import *
import sys
import os

SERVERNAME = 'CCTDAC_Pulser'
PREC_BITS = 16.
MAX_QUEUE_SIZE = 1000
SIGNALID = 270837

NUMCHANNELS = 28

# Nominal analog voltage range. Just used if there's no calibration available
NOMINAL_VMIN = -10.
NOMINAL_VMAX = 10.


class Voltage(object):
    def __init__(self, n, v):
        self.voltage = v
        self.portNum = n
        
class AnalogVoltage(Voltage):
    def __init__(self, n, v):
        super(AnalogVoltage, self).__init__(n, v)
        self.type = 'analog'

class DigitalVoltage(Voltage):
    def __init__(self, n, v):
        super(DigitalVoltage, self).__init__(n, v)
        self.type = 'digital'

class Port():
    """
    Store information about ports
    """
    def __init__(self, portNumber, calibrationCoeffs = None):
        self.portNumber = portNumber
        self.analogVoltage = None
        self.digitalVoltage = None

        """
        calibrationCoeffs is a list of the form [c0, c1, ..., cn]
        such that

        dv = c0 + c1*(av) + c2*(av)**2 + ... + cn*(av)**n

        """

        if not calibrationCoeffs:
            self.coeffs = [2**(PREC_BITS - 1), float(2**(PREC_BITS))/(NOMINAL_VMAX - NOMINAL_VMIN) ]
        else:
            self.coeffs = calibrationCoeffs
        print 'Coeff.Ch'+str(portNumber)+': '+str(self.coeffs)
        
    def setVoltage(self, v):
        if v.type == 'analog':
            self.analogVoltage = float(v.voltage)
            
            dv = int(round(sum( [ self.coeffs[n]*self.analogVoltage**n for n in range(len(self.coeffs)) ] )))
            print 'Analog Voltage Value: '+str(self.analogVoltage)
            print 'Digital Voltage Value: '+str(dv)
            if dv < 0:
                self.digitalVoltage = 0 # Set to the minimum acceptable code
            elif dv > ( 2**PREC_BITS - 1 ): # Largest acceptable code
                self.digitalVoltage = (2**PREC_BITS - 1)
            else:
                self.digitalVoltage = dv

        if v.type == 'digital':
            dv = int(v.voltage)
            if dv < 0:
                self.digitalVoltage = 0
                self.analogVoltage = NOMINAL_VMIN
            elif dv > ( 2**PREC_BITS - 1 ):
                self.digitalVoltage = (2**PREC_BITS - 1)
                self.analogVoltage = NOMINAL_VMAX
            else:
                self.digitalVoltage = dv
        
class CCTDACServer( LabradServer ):
    """
CCTDAC Server
Used for controlling DC trap electrodes

portList always holds the _most recent_ values. If a list cannot be written
because the serial port is unavailable, the portList is copied (by value!) to
the queue, and the portList can be safely updated.
"""

    name = SERVERNAME
    serNode = 'cctmain'
    onNewUpdate = Signal(SIGNALID, 'signal: ports updated', 's')

    @inlineCallbacks
    def initServer( self ):
	self.createInfo() # Populate list of Channels
	self.queue = []
	self.portlist = []
	if not self.serNode: raise SerialDeviceError( 'Must define serNode' )
	from labrad.wrappers import connectAsync
	cxn = yield connectAsync()
	self.pulser = cxn.pulser
	self.listeners = set()
	self.free = True
            
    @inlineCallbacks
    def createInfo( self ):
        """
        Initialize channel list
        """
        registry = self.client.registry
        degreeOfCalibration = 2 # 1st order fit. update this to auto-detect 
        self.portList = []
        yield registry.cd(['', 'Calibrations'])
        subs, keys = yield registry.dir()
        print 'Calibrated channels: '
        print subs
#        for i in range(1, NUMCHANNELS + 1): # Port nums are indexed from 1 in the microcrontroller
#            #registry.cd(['', 'Calibrations'])
#            print i
#            c = [] # list of calibration coefficients in form [c0, c1, ..., cn]
#            if str(i) in subs:
#                #print str(i)
#                yield registry.cd(['', 'Calibrations', str(i)])
#                for n in range( degreeOfCalibration + 1):
#                    e = yield registry.get( 'c'+str(n) )
#                    #print e
#                    c.append(e)
#                #c = [ registry.get( 'c'+str(n) ) for n in range( degreeOfCalibration + 1 )]
#                self.portList.append(Port(i, c))
#            else:
#                self.portList.append(Port(i)) # no preset calibration
        for i in range(1, NUMCHANNELS + 1):
            self.portList.append(Port(i))
        for p in self.portList:
            p.analogVoltage = 0
            
    @inlineCallbacks
    def tryToUpdate( self, c, v ):
        if self.free:
            self.free = False
            yield self.sendToPulser(c, v)
        elif len( self.queue ) > MAX_QUEUE_SIZE:
            print 'ERROR: Max queue size'
        else:
            self.queue.append( v)
        
    @inlineCallbacks
    def checkQueue( self, c ):
        if self.queue:
            print 'clearing queue...(%d items)' % len( self.queue )
            yield self.sendToPulser(c, self.queue.pop( 0 ))
        else:
            print 'queue free for writing'
            self.free = True

    @inlineCallbacks
    def sendToPulser(self, c, voltage):
        pulser = self.pulser
        yield self.pulser.reset_fifo_dac()
        for v in voltage:
            self.portList[v.portNum - 1].setVoltage(v)
            portNum = v.portNum
            p = self.portList[portNum - 1]
            codeInDec = int(p.digitalVoltage)
            print "codeInDec ", codeInDec
            print 'channel', portNum
	    stry = self.getHexRep(portNum, 1, codeInDec)
	    yield self.pulser.set_dac_voltage(stry)
	    print stry
	#yield self.pulser.set_dac_voltage('\xff\xff\x02\x08')
	#print '\xff\xff\x02\x08'
	yield self.pulser.set_dac_voltage('\x00\x00\x00\x00')    
        self.notifyOtherListeners(c)
        yield self.checkQueue(c)
                        
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
        
    def getHexRep(self, channel, setindex, value):
        chan=[]
        for i in range(5):
            chan.append(None)
        chan = self.f(channel, chan)
        print chan
        
        sety=[]
        for i in range(10):
            sety.append(None)
        sety = self.f(setindex, sety)
        print sety
        
        val=[]
        for i in range(16):
            val.append(None)
        val = self.f(value, val)
        print val
        
        big = val + chan + sety 
        big.append(False)

        return self.g(big[8:16]) + self.g(big[:8]) + self.g(big[24:32]) + self.g(big[16:24])
        
    def f(self, num, listy): #binary representation of values in the form of a list
        for i in range(len(listy)):
            if num >= 2**(len(listy)-1)/(2**i):
                listy[i] = True
                num -= 2**(len(listy)-1)/(2**i)
            else:
                listy[i] = False 
        return listy
        
    def g(self, listy):
	num = 0
	for i in range(8):
		if listy[i]:
			num += 2**7/2**i
	return chr(num)

    @setting( 0 , 'set digital voltages', returns = '' )
    def setDigitalVoltages( self, c, digitalVoltages ):
        """
	Pass digitalVoltages, a list of digital voltages to update.
	Currently, there must be one for each port.
	"""
        newVoltages = []
        for (n, dv) in zip(range(1, NUMCHANNELS + 1), digitalVoltages):
            newVoltages.append( DigitalVoltage(n, dv) )
        self.tryToUpdate(c, newVoltages )
        

    @setting( 1 , 'set analog voltages', analogVoltages='*v', returns = '' )
    def setAnalogVoltages( self, c, analogVoltages ):
        """
	Pass analogVoltages, a list of analog voltages to update.
	Currently, there must be one for each port.
	"""
        newVoltages = []
        for (n, av) in zip(range(1, NUMCHANNELS + 1), analogVoltages):
            newVoltages.append( AnalogVoltage(n, av) )
            yield self.tryToUpdate(c, newVoltages )
            newVoltages = []
 

    @setting( 2, 'set individual analog voltages', analogVoltages = '*(iv)', returns = '')
    def setIndivAnaVoltages(self, c, analogVoltages ):
        """
	Pass a list of tuples of the form:
	(portNum, newVolts)
	"""
        newVoltages = []
        for (num, av) in analogVoltages:
            newVoltages.append( AnalogVoltage(num, av) )
        yield self.tryToUpdate(c, newVoltages )
        
    @setting( 8, 'set individual digital voltages', digitalVoltages = '*(iv)', returns = '')
    def setIndivDigVoltages(self, c, digitalVoltages):
        """
	Pass a list of tuples of the form:
	(portNum, newVolts)
	"""        
        newVoltages = []
        for (num, dv) in digitalVoltages:
            newVoltages.append( DigitalVoltage(num, dv) )
        yield self.tryToUpdate(c, newVoltages )

    @setting( 3, 'get analog voltages', returns = '*v' )
    def getAnalogVoltages(self, c):
        """
	Return a list of the analog voltages currently in portList
	"""
        return [ p.analogVoltage for p in self.portList ] # Yay for list comprehensions

    @setting( 4, 'get digital voltages' )
    def getDigitalVoltages(self, c):
        """
	Return a list of digital voltages currently in portList
	"""
        return [ dv for v in [ p.digitalVoltage for p in self.portList ] ]
    
    @setting( 5, 'set multipole control file', file='s: multipole control file')
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
        
    @setting( 6, 'set multipole voltages', ms = '*(sv): dictionary of multipole voltages')
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
            realVolts += dot(multipoleSet[key],self.multipoleVectors[key])
        self.setAnalogVoltages(c, realVolts)
    
    @setting( 7, 'get multipole voltages',returns='*(s,v)')
    def getMultipoleVolgates(self, c):
        return self.multipoleSet.items()
       
if __name__ == "__main__":
    from labrad import util
    util.runServer( CCTDACServer() )
