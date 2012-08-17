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
from numpy import *
import sys

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
            
        yield self.registry.cd(['', 'cctdac_pulser', 'Cfile'])
        Cpath = yield self.registry.get('MostRecent1')
        yield self.setMultipoleControlFile(0, 1, Cpath)
        Cpath = yield self.registry.get('MostRecent2')
        yield self.setMultipoleControlFile(0, 2, Cpath)        
        yield self.registry.cd(['', 'cctdac_pulser', 'Multipoles'])
        ms = yield self.registry.get('Multipole Set')
        yield self.setMultipoleVoltages(0, ms)        

    @inlineCallbacks
    def sendToPulser(self, c, voltage):
        self.pulser.reset_fifo_dac()
        for v in voltage:
            self.portList[v.portNum - 1].setVoltage(v)
            portNum = v.portNum
            p = self.portList[portNum - 1]
            codeInDec = int(p.digitalVoltage)
	    stry = self.getHexRep(portNum, 1, codeInDec)
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

    @setting( 1 , "Set Analog Voltages", analogVoltages = '*v', returns = '' )
    def setAnalogVoltages( self, c, analogVoltages ):
        """
	    Pass analogVoltages, a list of analog voltages to update.
	    Currently, there must be one for each port.
	    """        
        li = []
        for (n, av) in zip(range(1, NUMCHANNELS + 1), analogVoltages):
            li.append((n, av))
        yield self.setIndivAnaVoltages(c, li)

    @setting( 2, "Set Individual Digital Voltages", digitalVoltages = '*(iv)', returns = '')
    def setIndivDigVoltages(self, c, digitalVoltages):
        """
        Pass a list of tuples of the form:
        (portNum, newVolts)
        """        
        for (num, dv) in digitalVoltages:
            yield self.sendToPulser(c, [DigitalVoltage(num, dv)] )        

    @setting( 3, "Set Individual Analog Voltages", analogVoltages = '*(iv)', returns = '')
    def setIndivAnaVoltages(self, c, analogVoltages ):
        """
	    Pass a list of tuples of the form:
	    (portNum, newVolts)
	    """
        for (num, av) in analogVoltages:
            yield self.sendToPulser(c, [AnalogVoltage(num, av)] )

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
    
    @setting( 6, "Set Multipole Control File", index = 'i', file = 's: multipole file location', returns = '')
    def setMultipoleControlFile(self, c, index, file):
        """
	    Read in a matrix of multipole values
	    """
        data = genfromtxt(file)
        vectors = {}
        vectors['Ex1'] = data[:,0]
        vectors['Ey1'] = data[:,1]
        vectors['Ez1'] = data[:,2]
        vectors['U1'] = data[:,3]
        vectors['U2'] = data[:,4]
        vectors['U3'] = data[:,5]
        vectors['U4'] = data[:,6]
        vectors['U5'] = data[:,7]
        try:
            vectors['Ex2'] = data[:,8]
            vectors['Ey2'] = data[:,9]
            vectors['Ez2'] = data[:,10]
            vectors['V1'] = data[:,11]
            vectors['V2'] = data[:,12]
            vectors['V3'] = data[:,13]
            vectors['V4'] = data[:,14]
            vectors['V5'] = data[:,15]
            wells = 2
        except: wells = 1

        if index == 1:
            self.multipoleVectors1 = {}
            for key in vectors.keys():
                self.multipoleVectors1[key] = vectors[key]
            print 'new primary Cfile: ' + file
            yield self.registry.cd(['', 'cctdac_pulser', 'Cfile'])
            yield self.registry.set('MostRecent1', file)                
        if index == 2:
            self.multipoleVectors2 = {}
            for key in vectors.keys():
                self.multipoleVectors2[key] = vectors[key]
            print 'new secondary Cfile: ' + file
            yield self.registry.cd(['', 'cctdac_pulser', 'Cfile'])
            yield self.registry.set('MostRecent2', file)              
        print 'num. wells: ' + str(wells) + '\n'

    @setting( 7, "Return Number Wells", returns = 'i')
    def returnNumWells(self, c):
        """
        Return the number of wells as determined by the size of the current Cfile
        """
        return self.numWells                               

    @setting( 8, "Set Multipole Voltages", ms = '*(sv): dictionary of multipole voltages')
    def setMultipoleVoltages(self, c, ms):
        """
	    set should be a dictionary with keys 'Ex', 'Ey', 'U1', etc.
	    """
        self.multipoleSet = {}
        for (k,v) in ms:
            self.multipoleSet[k] = v
        
        realVolts = zeros(NUMCHANNELS)
        for i in range(5):
            realVolts[i] = self.portList[i].analogVoltage            

        for key in self.multipoleVectors1.keys():
            realVolts += dot(self.multipoleSet[key], self.multipoleVectors1[key])
        self.setAnalogVoltages(c, realVolts)
        
        yield self.registry.cd(['', 'cctdac_pulser', 'Multipoles'])
        yield self.registry.set('Multipole Set', ms)
    
    @setting( 9, "Get Multipole Voltages",returns='*(s,v)')
    def getMultipoleVolgates(self, c):
        """
        Return a list of multipole voltages
        """
        return self.multipoleSet.items()
        
    @setting( 11, "Interpolate", A = 'v: constant between 0 and 1')
    def interpolate(self, c, A):
        A = float(A)           
        realVolts = zeros(NUMCHANNELS)
        for i in range(5):
            realVolts[i] = self.portList[i].analogVoltage
            
        self.multipoleVectorsA = {}             
        for key in self.multipoleVectors1.keys():
            self.multipoleVectorsA[key] = (1 - A) * self.multipoleVectors1[key] + A * self.multipoleVectors2[key]

        for key in self.multipoleVectorsA.keys():
            realVolts += dot(self.multipoleSet[key],self.multipoleVectorsA[key])
        yield self.setAnalogVoltages(c, realVolts)        
        
    @setting( 12, "Shuttle Ion", position = 'i: position to move to', steps = 'i: number of steps')
    def shuttleIon(self, c, position, steps):
        for i in range(1, steps + 1):                         
            yield self.interpolate(c, i/float(steps))
            time.sleep(1) 
                    	       
if __name__ == "__main__":
    from labrad import util
    util.runServer( CCTDACServer() )
