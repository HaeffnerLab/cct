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

SERVERNAME = 'CCTDAC_Pulser'
PREC_BITS = 16.
SIGNALID = 270837
NUMCHANNELS = 28
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
        
class CCTDACServer( LabradServer ):
    """
    CCTDAC Server
    Used for controlling DC trap electrodes
    """
    name = SERVERNAME
    serNode = 'cctmain'
    onNewUpdate = Signal(SIGNALID, 'signal: ports updated', 's')
    numWells = 1
    maxIndex = 1000
    curPosition = 0
    startIndex = 1
    stopIndex = 2
    multipoles = ['Ex1', 'Ey1', 'Ez1', 'U1', 'U2', 'U3', 'U4', 'U5']
    reset = 1
    
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
        """
        Initialize channel list
        """        
        self.portList = []        
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
                self.portList.append(Port(i, c))
            else:
                self.portList.append(Port(i)) # no preset calibration
        for p in self.portList:
            p.analogVoltage = 0
        
        yield self.advDACs()
        self.reset = 0
        yield self.registry.cd(['', 'cctdac_pulser', 'Cfile'])
        Cpath = yield self.registry.get('MostRecent')
        yield self.setMultipoleControlFile(0, Cpath)       
        yield self.registry.cd(['', 'cctdac_pulser', 'Multipoles'])
        ms = yield self.registry.get('Multipole Set')
        yield self.setMultipoleValues(0, ms)   

    @inlineCallbacks
    def sendToPulser(self, c, voltage, setIndex = 1):
        print setIndex
        self.pulser.reset_fifo_dac()
        for v in voltage:
            self.portList[v.portNum - 1].setVoltage(v)
            portNum = v.portNum
            p = self.portList[portNum - 1]
            codeInDec = int(p.digitalVoltage)
	    stry = self.getHexRep(portNum, setIndex, codeInDec)
        yield self.pulser.set_dac_voltage(stry)	    	
#        yield self.pulser.set_dac_voltage('\x00\x00\x00\x00')
        self.notifyOtherListeners(c)
                        
    def initContext(self, c):
        self.listeners.add(c.ID)

    def expireContext(self, c):
        self.listeners.remove(c.ID)
    
    def notifyOtherListeners(self, context):   
        notified = self.listeners.copy()
        try: notified.remove(context.ID)
        except: pass
        self.onNewUpdate('Channels updated', notified)      
        
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
        
        big = val + chan + sety + [False]
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
        for (num, dv) in digitalVoltages:
            yield self.sendToPulser(c, [DigitalVoltage(num, dv)] )        

    @setting( 3, "Set Individual Analog Voltages", analogVoltages = '*(iv)', setIndex = 'i', returns = '')
    def setIndivAnaVoltages(self, c, analogVoltages, setIndex = startIndex):
        """
	    Pass a list of tuples of the form:
	    (portNum, newVolts)
	    """
        print self.startIndex
        for (num, av) in analogVoltages:	   
            yield self.sendToPulser(c, [AnalogVoltage(num, av)], setIndex ) ###!!! setindex --> self.startIndex

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
        
        yield self.registry.cd(['', 'cctdac_pulser', 'Multipoles'])
        yield self.registry.set('Multipole Set', ms)
    
    @setting( 9, "Get Multipole Voltages",returns='*(s,v)')
    def getMultipoleVolgates(self, c):
        """
        Return a list of multipole voltages
        """
        return self.multipoleSet.items()

    @setting( 12, "Shuttle Ion", position = 'i: position to move to', returns = 'v')
    def shuttleIon(self, c, position):    
        n = self.startIndex
        if position > self.curPosition:
            for i in range(self.curPosition, position):
                yield self.setVoltages(c, i + 1, n)
                if n == self.maxIndex: n = 1
                else: n += 1                                
        elif position < self.curPosition:
            for i in range(position, self.curPosition)[::-1]:
                yield self.setVoltages(c, i, n)
                if n == self.maxIndex: n = 1
                else: n += 1   
        self.stopIndex = n-1
        if self.stopIndex == 0: self.stopIndex = self.maxIndex
        yield self.advDACs()
        self.startIndex = self.stopIndex
        p = self.pos[self.curPosition]
        returnValue( p )
        
        
    @inlineCallbacks
    def advDACs(self):
        """Pulse Sequence"""
        pulser = yield self.pulser
        seq = ADV_DAC(pulser)        
        pulser.new_sequence()
        params = {
                  'startIndex': self.startIndex,
                  'stopIndex': self.stopIndex,
                  'maxIndex': self.maxIndex,
                  'duration': 10e-8,
                  'reset': self.reset
                 }
        seq.setVariables(**params)
        seq.defineSequence()
        pulser.program_sequence()
        pulser.start_single()
        pulser.wait_sequence_done()
        pulser.stop_sequence()
        pulser.reset_timetags()            
        
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
        
    @setting(15, "do nothing")
    def doNone(self, c):
        pass
                
if __name__ == "__main__":
    from labrad import util
    util.runServer( CCTDACServer() )
