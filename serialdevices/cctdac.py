'''
### BEGIN NODE INFO
[info]
name = CCTDAC
version = 1.1
description = 
instancename = CCTDAC

[startup]
cmdline = %PYTHON% %FILE%
timeout = 20

[shutdown]
message = 987654321
timeout = 20

### END NODE INFO
'''
#Adapted from laserdacbox.py


from serialdeviceserver import SerialDeviceServer, setting, inlineCallbacks, SerialDeviceError, SerialConnectionError, PortRegError
from twisted.internet import reactor
from twisted.internet.defer import returnValue
import binascii
from labrad.server import Signal
import copy as cpy # copy objects by value
from numpy import *
import sys
import os
import time

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
NOMINAL_VMIN = -40.0
NOMINAL_VMAX = 40.0

class DCBoxError( SerialConnectionError ):
    errorDict = {
        0:'Invalid channel name',
        1:'Voltage out of range',
        2:'Queue size exceeded',
        3:'Shutter input must be boolean',
        4:'Must set value before you can retrieve',
        5:'Correct response from DC box not received, sleeping for short period'
        }


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
            print 'Analog Voltage Value: '+str(self.analogVoltage) #\033[1;33mYellow like Yolk\033[1;m
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
                print dv
                self.digitalVoltage = dv
        
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

        
        yield self.createInfo() # Populate list of Channels
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
        registry = self.client.registry        
        yield registry.cd(['', 'cctdac', 'Multipoles'])
        ms = yield registry.get('Multipole Set')
        yield self.setMultipoleVoltages(0, ms)      
        #Ex = yield registry.get('Ex')
        #Ey = yield registry.get('Ey')
        #Ez = yield registry.get('Ez')
        #U1 = yield registry.get('U1')
        #U2 = yield registry.get('U2')
        #U3 = yield registry.get('U3')
        #U4 = yield registry.get('U4')
        #U5 = yield registry.get('U5')        
        #yield self.setMultipoleVoltages(0, [('Ex1', Ex), ('Ey1', Ey), ('Ez1', Ez), ('U1', U1), ('U2', U2), ('U3', U3), ('U4', U4), ('U5', U5)])           
	
        
    
    @inlineCallbacks
    def createInfo( self ):
        """
        Initialize channel list
        """
        self.init = True
        registry = self.client.registry
        degreeOfCalibration = 2 # 1st order fit. update this to auto-detect 
        self.portList = []
        yield registry.cd(['', 'cctdac', 'Calibrations'])
        subs, keys = yield registry.dir()
        print 'Calibrated channels: '
        print subs
        for i in range(1, NUMCHANNELS + 1): # Port nums are indexed from 1 in the microcrontroller
            #registry.cd(['', 'Calibrations'])
            c = [] # list of calibration coefficients in form [c0, c1, ..., cn]
            if str(i) in subs:
                #print str(i)
                yield registry.cd(['', 'cctdac', 'Calibrations', str(i)])
                for n in range( degreeOfCalibration + 1):
                    e = yield registry.get( 'c'+str(n) )
                    #print e
                    c.append(e)
                #c = [ registry.get( 'c'+str(n) ) for n in range( degreeOfCalibration + 1 )]
                self.portList.append(Port(i, c))
            else:
                self.portList.append(Port(i)) # no preset calibration
	yield registry.cd(['', 'cctdac', 'Cfile'])
	Cpath = yield registry.get('MostRecent')
	yield self.setMultipoleControlFile(0, Cpath)
        #ms = yield registry.get('Multipole Set')
        #yield self.setMultipoleVoltages(0, [('U5',0.0),('U4',0.0),('U1',-0.22),('Ez1',0.0),('U3',-0.22),('U2',4.5),('Ey1',0.0),('V1',-0.22),('V2',4.5),('Ey2',0.0),('Ex2',0.0),('Ez2',0.0),('V3',0.22),('Ex1',0.0),('V4',4.0),('V5',0.0)])	
        
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
    def tryToUpdate( self, c, voltages ):
        """
Check if serial connection is free.
If free, write the list of ports to the DAC.
If not free, store the port list in the queue.
Raise error when queue fills up.
@param channel: Channel to write to
@param value: Value to write
@raise DCBoxError: Error code 2. Queue size exceeded
"""
        if self.free:
            self.free = False
            yield self.writeToSerial(c, voltages )
            
        elif len( self.queue ) > MAX_QUEUE_SIZE:
            raise DCBoxError( 2 )
        else:
            self.queue.append( voltages )
            

    @inlineCallbacks
    def writeToSerial( self, c, voltages ):
        """
Write value to specified channel through serial connection.
Convert message to microcontroller's syntax.

There's currently no confirmation from the DAC, so we assume everything's worked.
We'll prob want to make the DAC confirm a successful update

After the list has been written, update the current portList
"""
        self.checkConnection()

        for v in voltages:
            self.portList[v.portNum - 1].setVoltage(v)
        toSend = self.makeComString( voltages )
        time.sleep(0.3)
        yield self.ser.write( toSend )
        self.notifyOtherListeners(c)
        yield self.checkQueue(c)

    def makeComString(self, voltages):
        """
Pass a list of Port objects to update. The updated value must already be written to the Port.

Construct a com string in the appropriate format.
"""
        numPortsChanged = len( voltages )
        setNum = 1
        
        nChanged = binascii.unhexlify(hex(numPortsChanged)[2:].zfill(2)) # Number of ports to change
        comstr = nChanged
        for v in voltages:
            portNum = v.portNum
            p = self.portList[portNum - 1]
            codeInDec = int(p.digitalVoltage)
            print "codeInDec ", codeInDec
            port = binascii.unhexlify(hex(portNum)[2:].zfill(2)) # Which port to change
            setn = binascii.unhexlify(hex(setNum)[2:].zfill(4)) # Which set of updates are we applying ( = 1 for now, always)
            code = binascii.unhexlify(hex(codeInDec)[2:].zfill(4)) # What digital code to write to the port
            comstr += 'P' + port + 'I' + setn + ',' + code
        print 'Serial String: '+str(comstr)
        return comstr
    
    def initContext(self, c):
        self.listeners.add(c.ID)
    
    def expireContext(self, c):
        self.listeners.remove(c.ID)
    
    def notifyOtherListeners(self, context):
        """
Notifies all listeners except the one in the given context
"""	
        if self.init:
	    self.init = False
	    return
        notified = self.listeners.copy()
        try: notified.remove(context.ID)
        except: print 'no context'
        self.onNewUpdate('Channels updated', notified)
        print "Notifyin' them listeners"
    
    @setting( 0 , 'Set Digital Voltages', returns = '' )
    def setDigitalVoltages( self, c, digitalVoltages ):
        """
Pass digitalVoltages, a list of digital voltages to update.
Currently, there must be one for each port.
"""
        newVoltages = []
        for (n, dv) in zip(range(1, NUMCHANNELS + 1), digitalVoltages):
            newVoltages.append( DigitalVoltage(n, dv) )
        self.tryToUpdate(c, newVoltages )
        

    @setting( 1 , 'Set Analog Voltages', analogVoltages='*v', returns = '' )
    def setAnalogVoltages( self, c, analogVoltages ):
        """
Pass analogVoltages, a list of analog voltages to update.
Currently, there must be one for each port.
"""
        newVoltages = []
        for (n, av) in zip(range(1, NUMCHANNELS + 1), analogVoltages):
            newVoltages.append( AnalogVoltage(n, av) )
        yield self.tryToUpdate(c, newVoltages )
 

    @setting( 2, 'Set Individual Analog Voltages', analogVoltages = '*(iv)', returns = '')
    def setIndivAnaVoltages(self, c, analogVoltages ):
        """
Pass a list of tuples of the form:
(portNum, newVolts)
"""
        newVoltages = []
        for (num, av) in analogVoltages:
            newVoltages.append( AnalogVoltage(num, av) )
        yield self.tryToUpdate(c, newVoltages )
        
    @setting( 8, 'Set Individual Digital Voltages', digitalVoltages = '*(iv)', returns = '')
    def setIndivDigVoltages(self, c, digitalVoltages):
        newVoltages = []
        for (num, dv) in digitalVoltages:
            newVoltages.append( DigitalVoltage(num, dv) )
        yield self.tryToUpdate(c, newVoltages)

    @setting( 3, 'Get Analog Voltages', returns = '*v' )
    def getAnalogVoltages(self, c):
        """
Return a list of the analog voltages currently in portList
"""
        return [ p.analogVoltage for p in self.portList ] # Yay for list comprehensions

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
        yield registry.cd(['', 'cctdac', 'Cfile'])
        yield registry.set('MostRecent', file)
        print file
        
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
        
        registry = self.client.registry
        yield registry.cd(['', 'cctdac', 'Multipoles'])
        yield registry.set('Multipole Set', ms)        
        #yield registry.set('Ex', multipoleSet['Ex'])
        #yield registry.set('Ey', multipoleSet['Ey'])
        #yield registry.set('Ez', multipoleSet['Ez'])
        #yield registry.set('U1', multipoleSet['U1'])
        #yield registry.set('U2', multipoleSet['U2'])
        #yield registry.set('U3', multipoleSet['U3'])
        #yield registry.set('U4', multipoleSet['U4'])
        #yield registry.set('U5', multipoleSet['U5'])        
    
    @setting( 7, 'Get Multipole Voltages',returns='*(s,v)')
    def getMultipoleVolgates(self, c):
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


