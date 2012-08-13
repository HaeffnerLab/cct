'''
### BEGIN NODE INFO
[info]
name = CCTDAC Pulser
version = 1.0
description = 
instancename = CCTDAC Pulser

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
import copy as cpy 
from numpy import *
import sys
import os
import time

SERVERNAME = 'CCTDAC_Pulser'
PREC_BITS = 16.
MAX_QUEUE_SIZE = 1000
SIGNALID = 270837

NUMCHANNELS = 28

# Nominal analog voltage range. Just used if there's no calibration available
NOMINAL_VMIN = -40.
NOMINAL_VMAX = 40.


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
    
    calibrationCoeffs is a list of the form [c0, c1, ..., cn]
    such that
    dv = c0 + c1*(av) + c2*(av)**2 + ... + cn*(av)**n
    """
    def __init__(self, portNumber, calibrationCoeffs = None):
        self.portNumber = portNumber
        self.analogVoltage = None
        self.digitalVoltage = None
        if not calibrationCoeffs:
            self.coeffs = [2**(PREC_BITS - 1), float(2**(PREC_BITS))/(NOMINAL_VMAX - NOMINAL_VMIN) ]
        else:
            self.coeffs = calibrationCoeffs
        print 'Coeff.Ch'+str(portNumber)+': '+str(self.coeffs)
        
    def setVoltage(self, v):
        if v.type == 'analog':
            self.analogVoltage = float(v.voltage)
            print self.analogVoltage
            print sum( [ self.coeffs[n]*self.analogVoltage**n for n in range(len(self.coeffs)) ] )
            dv = int(round(sum( [ self.coeffs[n]*self.analogVoltage**n for n in range(len(self.coeffs)) ] )))
            print '\nChannel Value' + str(v.portNum)
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
    numWells = 1

    @inlineCallbacks
    def initServer( self ):
        self.free = True        
        self.queue = []
        self.portlist = []    
        from labrad.wrappers import connectAsync
        cxn = yield connectAsync()
        self.pulser = cxn.pulser        
        self.createInfo() 
        self.listeners = set()
            
    @inlineCallbacks
    def createInfo( self ):
        """
        Initialize channel list
        """        
        degreeOfCalibration = 3 # 1st order fit. update this to auto-detect 
        self.portList = []
        registry = self.client.registry
        yield registry.cd(['', 'cctdac_pulser', 'Calibrations'])
        subs, keys = yield registry.dir()
        print 'Calibrated channels: '
        for i in range(1, NUMCHANNELS + 1): # Port nums are indexed from 1
            c = [] # list of calibration coefficients in form [c0, c1, ..., cn]
            if str(i) in subs:
                yield registry.cd(['', 'cctdac_pulser', 'Calibrations', str(i)])
                for n in range( degreeOfCalibration + 1):
                    e = yield registry.get( 'c'+str(n) )                    
                    c.append(e)
                self.portList.append(Port(i, c))
            else:
                self.portList.append(Port(i)) # no preset calibration
        for p in self.portList:
            p.analogVoltage = 0
        yield registry.cd(['', 'cctdac_pulser', 'Cfile'])
        Cpath = yield registry.get('MostRecent')
        yield self.setMultipoleControlFile(0, Cpath)
        Cpath = yield registry.get('MostRecentSecondary')
        yield self.setSecondMultipoleControlFile(0, Cpath)        
        yield registry.cd(['', 'cctdac_pulser', 'Multipoles'])
        ms = yield registry.get('Multipole Set')
        yield self.setMultipoleVoltages(0, ms)        
        
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
        pulser.reset_fifo_dac()
        for v in voltage:
            self.portList[v.portNum - 1].setVoltage(v)
            portNum = v.portNum
            p = self.portList[portNum - 1]
            codeInDec = int(p.digitalVoltage)
	    stry = self.getHexRep(portNum, 1, codeInDec)
	    self.pulser.set_dac_voltage(stry)	    	
        self.pulser.set_dac_voltage('\x00\x00\x00\x00')
        print 'sent to pulser'
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
        try: notified.remove(context.ID)
        except: print "no context"
        self.onNewUpdate('Channels updated', notified)
        print "Notifyin' them listeners"        
        
    def getHexRep(self, channel, setindex, value):
        chan=[]
        for i in range(5):
            chan.append(None)
        chan = self.f(channel, chan)
        
        sety=[]
        for i in range(10):
            sety.append(None)
        sety = self.f(setindex, sety)
        
        val=[]
        for i in range(16):
            val.append(None)
        val = self.f(value, val)
        
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
        li = []
        for (n, av) in zip(range(1, NUMCHANNELS + 1), analogVoltages):
            li.append((n, av))
        self.setIndivAnaVoltages(c, li)

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

    @setting( 4, 'get digital voltages', returns = '*v' )
    def getDigitalVoltages(self, c):
        """
	    Return a list of digital voltages currently in portList
	    """
        return [ p.digitalVoltage for p in self.portlist ]
    
    @setting( 5, 'set multipole control file', file='s: multipole control file', returns = '')
    def setMultipoleControlFile(self, c, file):
        """
	    Read in a matrix of multipole values
	    """
        data = genfromtxt(file)
        self.multipoleVectors = {}
        self.multipoleVectors['Ex1'] = data[:,0]
        self.multipoleVectors['Ey1'] = data[:,1]
        self.multipoleVectors['Ez1'] = data[:,2]
        self.multipoleVectors['U1'] = data[:,3]
        self.multipoleVectors['U2'] = data[:,4]
        self.multipoleVectors['U3'] = data[:,5]
        self.multipoleVectors['U4'] = data[:,6]
        self.multipoleVectors['U5'] = data[:,7]
        try:
            self.multipoleVectors['Ex2'] = data[:,8]
            self.multipoleVectors['Ey2'] = data[:,9]
            self.multipoleVectors['Ez2'] = data[:,10]
            self.multipoleVectors['V1'] = data[:,11]
            self.multipoleVectors['V2'] = data[:,12]
            self.multipoleVectors['V3'] = data[:,13]
            self.multipoleVectors['V4'] = data[:,14]
            self.multipoleVectors['V5'] = data[:,15]
            self.numWells = 2
        except: self.numWells = 1
        print "num. wells: " + str(self.numWells)
        
        registry = self.client.registry
        yield registry.cd(['', 'cctdac_pulser', 'Cfile'])
        yield registry.set('MostRecent', file)
        
    @setting( 10, 'set second multipole control file', file='s: multipole control file', returns = '')
    def setSecondMultipoleControlFile(self, c, file):
        """
        Read in a matrix of multipole values
        """
        data = genfromtxt(file)
        self.multipoleVectors2 = {}
        self.multipoleVectors2['Ex1'] = data[:,0]
        self.multipoleVectors2['Ey1'] = data[:,1]
        self.multipoleVectors2['Ez1'] = data[:,2]
        self.multipoleVectors2['U1'] = data[:,3]
        self.multipoleVectors2['U2'] = data[:,4]
        self.multipoleVectors2['U3'] = data[:,5]
        self.multipoleVectors2['U4'] = data[:,6]
        self.multipoleVectors2['U5'] = data[:,7]
        try:
            self.multipoleVectors2['Ex2'] = data[:,8]
            self.multipoleVectors2['Ey2'] = data[:,9]
            self.multipoleVectors2['Ez2'] = data[:,10]
            self.multipoleVectors2['V1'] = data[:,11]
            self.multipoleVectors2['V2'] = data[:,12]
            self.multipoleVectors2['V3'] = data[:,13]
            self.multipoleVectors2['V4'] = data[:,14]
            self.multipoleVectors2['V5'] = data[:,15]
            self.numWells2 = 2
        except: self.numWells2 = 1
        print "num. wells(2): " + str(self.numWells)
        
        registry = self.client.registry
        yield registry.cd(['', 'cctdac_pulser', 'Cfile'])
        yield registry.set('MostRecentSecondary', file)
        
    @setting( 11, "Shuttle Ion", A = 'v: constant between 0 and 1')
    def shuttleIon(self, c, A):
        A = float(A)
        self.multipoleVectorsA = {}            
        realVolts = zeros(NUMCHANNELS)
        for i in range(5):
            realVolts[i] = self.portList[i].analogVoltage
 
        self.multipoleVectorsA['Ex1'] = self.multipoleVectors['Ex1'] + A * ( self.multipoleVectors2['Ex1'] - self.multipoleVectors['Ex1'] )
        self.multipoleVectorsA['Ey1'] = self.multipoleVectors['Ey1'] + A * ( self.multipoleVectors2['Ey1'] - self.multipoleVectors['Ey1'] )
        self.multipoleVectorsA['Ez1'] = self.multipoleVectors['Ez1'] + A * ( self.multipoleVectors2['Ez1'] - self.multipoleVectors['Ez1'] )
        self.multipoleVectorsA['U1'] = self.multipoleVectors['U1'] + A * ( self.multipoleVectors2['U1'] - self.multipoleVectors['U1'] )
        self.multipoleVectorsA['U2'] = self.multipoleVectors['U2'] + A * ( self.multipoleVectors2['U2'] - self.multipoleVectors['U2'] ) 
        self.multipoleVectorsA['U3'] = self.multipoleVectors['U3'] + A * ( self.multipoleVectors2['U3'] - self.multipoleVectors['U3'] )
        self.multipoleVectorsA['U4'] = self.multipoleVectors['U4'] + A * ( self.multipoleVectors2['U4'] - self.multipoleVectors['U4'] )
        self.multipoleVectorsA['U5'] = self.multipoleVectors['U5'] + A * ( self.multipoleVectors2['U5'] - self.multipoleVectors['U5'] )
        if self.numWells == 2:
            self.multipoleVectorsA['Ex2'] = self.multipoleVectors['Ex2'] + A * ( self.multipoleVectors2['Ex2'] - self.multipoleVectors['Ex2'] )
            self.multipoleVectorsA['Ey2'] = self.multipoleVectors['Ey2'] + A * ( self.multipoleVectors2['Ey2'] - self.multipoleVectors['Ey2'] ) 
            self.multipoleVectorsA['Ez2'] = self.multipoleVectors['Ez2'] + A * ( self.multipoleVectors2['Ez2'] - self.multipoleVectors['Ez2'] )
            self.multipoleVectorsA['V1'] = self.multipoleVectors['V1'] + A * ( self.multipoleVectors2['V1'] - self.multipoleVectors['V1'] ) 
            self.multipoleVectorsA['V2'] = self.multipoleVectors['V2'] + A * ( self.multipoleVectors2['V2'] - self.multipoleVectors['V2'] )
            self.multipoleVectorsA['V3'] = self.multipoleVectors['V3'] + A * ( self.multipoleVectors2['V3'] - self.multipoleVectors['V3'] ) 
            self.multipoleVectorsA['V4'] = self.multipoleVectors['V4'] + A * ( self.multipoleVectors2['V4'] - self.multipoleVectors['V4'] ) 
            self.multipoleVectorsA['V5'] = self.multipoleVectors['V5'] + A * ( self.multipoleVectors2['V5'] - self.multipoleVectors['V5'] )
            
        for key in self.multipoleVectorsA.keys():
            realVolts += dot(self.multipoleSet[key],self.multipoleVectorsA[key])
        self.setAnalogVoltages(c, realVolts)
        
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
        for i in range(5):
            try: realVolts[i] = self.portList[i].analogVoltage
            except: realVolts[i] = 0	
        print self.multipoleVectors.keys()
        for key in self.multipoleVectors.keys():
            realVolts += dot(multipoleSet[key],self.multipoleVectors[key])
        self.setAnalogVoltages(c, realVolts)
        
        registry = self.client.registry
        yield registry.cd(['', 'cctdac_pulser', 'Multipoles'])
        yield registry.set('Multipole Set', ms)
    
    @setting( 7, 'get multipole voltages',returns='*(s,v)')
    def getMultipoleVolgates(self, c):
        """
        Return a list of multipole voltages
        """
        return self.multipoleSet.items()
        
    @setting( 9, 'return number wells', returns = 'i')
    def returnNumWells(self, c):
        """
	    Return the number of wells as determined by the size of the current Cfile
        """
        return self.numWells
	       
if __name__ == "__main__":
    from labrad import util
    util.runServer( CCTDACServer() )
