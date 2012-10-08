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
from scipy import interpolate
from scipy.interpolate import UnivariateSpline as UniSpline
from time import *
from numpy import *
import sys
sys.path.append('/home/cct/LabRAD/cct/PulseSequences')
from advanceDACs import ADV_DAC

SERVERNAME = 'CCTDAC Pulser'
PREC_BITS = 16.
SIGNALID = 270837
NUMCHANNELS = 28
NOMINAL_VMIN = -40.
NOMINAL_VMAX = 40.

class Voltage(object):
    def __init__(self, n, i, v):        
        self.portNum = n
        self.setNum = i
        self.voltage = v
        
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
    def __init__(self, portNumber, physicalChannel = None, calibrationCoeffs = None):        
        self.portNumber = portNumber
        if physicalChannel is not None:
            self.physicalChannel = physicalChannel
        else:
            self.physicalChannel = portNumber
        self.analogVoltage = None
        self.digitalVoltage = None
        self.hexRep = None
        if not calibrationCoeffs:
            self.coeffs = [2**(PREC_BITS - 1), float(2**(PREC_BITS))/(NOMINAL_VMAX - NOMINAL_VMIN) ]
        else:
            self.coeffs = calibrationCoeffs
        
    def setVoltage(self, v):
        if v.type == 'analog':
            self.analogVoltage = float(v.voltage)
            dv = int(round(sum( [ self.coeffs[n]*self.analogVoltage**n for n in range(len(self.coeffs)) ] )))
            print 'Channel: ' + str(v.portNum)
            print 'Analog Voltage Value: '+str(self.analogVoltage)
            print 'Digital Voltage Value: '+str(dv) + '\n'
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
                
        self.hexRep = self.getHexRep(v.setNum, v.physicalChannel, dv)
    
    def getHexRep(self, setNum, portNum, value):
        port = self.f(portNum, 5)
        set = self.f(setindex, 10)
        value = self.f(value, 16)        
        big = value + port + set + [False]
        return self.g(big[8:16]) + self.g(big[:8]) + self.g(big[24:32]) + self.g(big[16:24])
            
    def f(self, num, length): #binary representation of values in the form of a list
        listy = [None for i in range(length)]
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
                
        
        
class CCTDACServer( LabradServer ):
    """
    CCTDAC Server
    Used for controlling DC trap electrodes
    """
    name = SERVERNAME
    serNode = 'cctmain'
    onNewUpdate = Signal(SIGNALID, 'signal: ports updated', 's')
    maxIndex = 126    
    multipoles = ['Ex1', 'Ey1', 'Ez1', 'U1', 'U2', 'U3', 'U4', 'U5']
    startIndex = 1
    stopIndex = 2        
    
    @inlineCallbacks
    def initServer( self ):  
        from labrad.wrappers import connectAsync
        cxn = yield connectAsync()
        self.pulser = cxn.pulser
        self.registry = self.client.registry        
        self.createInfo() 
        self.listeners = set()
            
    @inlineCallbacks
    def createInfo( self ):             
        self.portList = []
        ''' See if there's a map between digital channels and analog channels.    
        cctdac.conf should be of the form:
        (software channel) -> (hardware channel)
        '''
        try:
            with open('cctdac.conf') as f:
                mappedChannels = []
                for c in f: # iterate line by line
                    map = c.split('->')
                    mappedChannels.append( [int(map[0]), int(map[1])] ) # [softChan, hardChan]
        except IOError as e:
            print "No port mapping found"    
                
        degreeOfCalibration = 3 # 1st order fit. update this to auto-detect 
        yield self.registry.cd(['', 'cctdac_pulser', 'Calibrations'])
        subs, keys = yield self.registry.dir()
        sbs = ''
        for s in subs:
            sbs += s + ', '
        print 'Calibrated channels: ' + sbs 
        for i in range(1, NUMCHANNELS + 1): # Port nums are indexed from 1
            c = [] # list of calibration coefficients in form [c0, c1, ..., cn]
            if str(i) in subs:
                yield self.registry.cd(['', 'cctdac_pulser', 'Calibrations', str(i)])
                for n in range( degreeOfCalibration + 1):
                    e = yield self.registry.get( 'c'+str(n) )                    
                    c.append(e)
                self.portList.append(Port(i, mappedChannels[i][1], c))
            else:
                self.portList.append(Port(i)) # no preset calibration
        for p in self.portList:
            p.analogVoltage = 0                
        yield self.advDACs(1)
        yield self.registry.cd(['', 'cctdac_pulser'])
        Cpath = yield self.registry.get('MostRecent')
        yield self.setMultipoleControlFile(0, Cpath)
        self.curPosition = yield self.registry.get('IonPosition')
        ms = yield self.registry.get('MultipoleSet')
        yield self.setMultipoleValues(0, ms)
           
        
    @inlineCallbacks
    def sendToPulser(self, c, voltage):
        self.pulser.reset_fifo_dac()
        self.portList[v.portNum - 1].setVoltage(v)
        yield self.pulser.set_dac_voltage(self.portList[v.portNum - 1].hexRep)            
        self.notifyOtherListeners(c)        
                        
    def initContext(self, c):
        self.listeners.add(c.ID)

    def expireContext(self, c):
        self.listeners.remove(c.ID)
    
    def notifyOtherListeners(self, context):   
        notified = self.listeners.copy()
        try: notified.remove(context.ID)
        except: print 'init?'
        self.onNewUpdate('Channels updated', notified)      

    @setting( 0 , "Set Digital Voltages", digitalVoltages = '*v', returns = '' )
    def setDigitalVoltages( self, c, digitalVoltages ):
        """
        Pass digitalVoltages, a list of digital voltages to update.
        Currently, there must be one for each port.
        """        
        li = []
        for (n, dv) in zip(range(1, NUMCHANNELS + 1), digitalVoltages):
            li.append((n, dv))
        self.setIndivDigVoltages(c, li)        

    @setting( 1 , "Set Analog Voltages", analogVoltages = '*v', setIndex = 'i', returns = '' )
    def setAnalogVoltages( self, c, analogVoltages, setIndex = startIndex):
        """
        Pass analogVoltages, a list of analog voltages to update.
        Currently, there must be one for each port.
        """        
        li = []
        for (n, av) in zip(range(1, NUMCHANNELS + 1), analogVoltages):
            li.append((n, av))
        yield self.setIndivAnaVoltages(c, li, setIndex)

    @setting( 2, "Set Individual Digital Voltages", digitalVoltages = '*(iv)', returns = '')
    def setIndivDigVoltages(self, c, digitalVoltages):
        """
        Pass a list of tuples of the form:
        (portNum, newVolts)
        """        
        for (portNum, dv) in digitalVoltages:
            yield self.sendToPulser(c, DigitalVoltage(portNum, setNum, dv) )        

    @setting( 3, "Set Individual Analog Voltages", analogVoltages = '*(iv)', setIndex = 'i', returns = '')
    def setIndivAnaVoltages(self, c, analogVoltages, setIndex = startIndex):
        """
        Pass a list of tuples of the form:
        (portNum, newVolts)
        """
        print self.startIndex
        for (num, av) in analogVoltages:      
            yield self.sendToPulser(c, AnalogVoltage(num, setIndex, av)) ###!!! setindex --> self.startIndex

    @setting( 4, "Get Digital Voltages", returns = '*v' )
    def getDigitalVoltages(self, c):
        """
        Return a list of digital voltages currently in portList
        """
        return [ p.digitalVoltage for p in self.portlist ]            

    @setting( 5, "Get Analog Voltages", returns = '*v' )
    def getAnalogVoltages(self, c):
        """
        Return a list of the analog voltages currently in portList
        """
        return [ p.analogVoltage for p in self.portList ] # Yay for list comprehensions
    
    @setting( 6, "Set Multipole Control File", file = 's')
    def setMultipoleControlFile(self, c, file):                
        data = genfromtxt(file)
        numCols = data.size / (23 * 8)
        numPositions = (numCols - 1) * 10.
        sp = {}
        spline = {}
        x = []
        for i in range(numCols): x.append(i)                      
        p = arange(0, (numCols -1) * (1 + 1/numPositions), (numCols - 1)/numPositions)
        
        n = 0
        for i in range(23):
            sp[i] = {}
            spline[i] = {}      
            for j in self.multipoles:                
                sp[i][j] = UniSpline(x, data[i + n], s = 0 )                
                spline[i][j] = sp[i][j](p)                                
                n += 23                           
            n = 0
        self.spline = spline
        #yield self.ShSetMultipoleVoltages(c, 0, 1)
        self.startIndex = 1
        
        y = data[23 * 8]        
        #fit = interp1d(x, y)
        fit = interpolate.interp1d(x, y, 'linear')
        self.pos = fit(p)        
        #from matplotlib import pyplot as p
        #for i in range(23):        
            #p.plot(spline[i]['U2'])
            #p.show()
        
    @setting( 7, "Return Number Wells", returns = 'i')
    def returnNumWells(self, c):
        """
        Return the number of wells as determined by the size of the current Cfile
        """
        return self.numWells     

    @setting( 8, "Set Multipole Values", ms = '*(sv): dictionary of multipole values')
    def setMultipoleValues(self, c, ms):
        """
        set should be a dictionary with keys 'Ex', 'Ey', 'U1', etc.
        """
        self.multipoleSet = {}
        for (k,v) in ms:
            self.multipoleSet[k] = v
            
        self.stopIndex = self.startIndex + 1
        if self.stopIndex > self.maxIndex: self.stopIndex = 1
        yield self.setVoltages(c, self.curPosition, self.stopIndex)
        yield self.advDACs()
        self.startIndex = self.stopIndex
        
        yield self.registry.cd(['', 'cctdac_pulser'])
        yield self.registry.set('MultipoleSet', ms)
    
    @setting( 9, "Get Multipole Voltages",returns='*(s,v)')
    def getMultipoleVolgates(self, c):
        """
        Return a list of multipole voltages
        """
        return self.multipoleSet.items()

    @setting( 12, "Shuttle Ion", position = 'i: position to move to')
    def shuttleIon(self, c, position):            
        n = self.startIndex
        if position > self.curPosition:
            for i in range(self.curPosition, position):
                yield self.setVoltages(c, i + 1, n)
                if n == 1:                    
                    self.advDACs(1)                    
                if n == self.maxIndex: n = 1                    
                else: n += 1                              
        elif position < self.curPosition:
            for i in range(position, self.curPosition)[::-1]:
                yield self.setVoltages(c, i, n)
                if n == 1:                    
                    self.advDACs(1)                                
                if n == self.maxIndex: n = 1
                else: n += 1   
        self.stopIndex = n-1
        if self.stopIndex == 0: self.stopIndex = self.maxIndex
        yield self.advDACs()
        self.startIndex = self.stopIndex
        
        yield self.registry.cd(['', 'cctdac_pulser'])
        yield self.registry.set('IonPosition', self.curPosition)  
                
    @inlineCallbacks
    def advDACs(self, reset = None):        
        """Pulse Sequence"""
        pulser = yield self.pulser
        seq = ADV_DAC(pulser)        
        pulser.new_sequence()
        params = {
                  'startIndex': self.startIndex,
                  'stopIndex': self.stopIndex,
                  'maxIndex': self.maxIndex,
                  'duration': 10e-4,
                  'reset': reset
                 }
        seq.setVariables(**params)
        seq.defineSequence()
        pulser.program_sequence()
        pulser.start_single()
        pulser.wait_sequence_done()
        pulser.stop_sequence()
        pulser.reset_timetags()
        if reset: self.startIndex = 1            
        
    @setting( 14, "Set Voltages", newPosition = 'i', index = 'i')
    def setVoltages(self, c, newPosition, index):        
        n = newPosition
        realVolts = zeros(NUMCHANNELS)
        for i in range(5):
            realVolts[i] = self.portList[i].analogVoltage  
        for i in range(23): 
            for j in self.multipoles:                   
                realVolts[i + 5] += self.spline[i][j][n] * self.multipoleSet[j] 
        yield self.setAnalogVoltages(c, realVolts, index)
        self.curIndex = index
        self.curPosition = n
        
    @setting(16, "Return Ion Info", returns = 'iv')
    def retIonIndex(self, c):
        return [self.curPosition, self.pos[self.curPosition]]
    
    @setting(17, "Reset Index")
    def rstIndex(self, c):
        self.stopIndex = 1
        self.startIndex = self.maxIndex-1
        yield self.advDACs()
        self.startIndex = 1
        
    @setting(15, "do nothing")
    def doNone(self, c):
        pass
                
if __name__ == "__main__":
    from labrad import util
    util.runServer( CCTDACServer() )
