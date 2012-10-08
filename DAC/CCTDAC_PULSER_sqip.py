'''
### BEGIN NODE INFO
[info]
name = DACserver
version = 1.0
description = 
instancename = DACserver

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
from scipy.interpolate import UnivariateSpline as UniSpline
from time import *
from numpy import *
import numpy
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
            self.coeffs = [2**(PREC_BITS - 1), float(2**(PREC_BITS))/(NOMINAL_VMAX - NOMINAL_VMIN) ]
        
    def setVoltage(self, v):
        if v.type == 'analog':
            self.analogVoltage = float(v.voltage)
            dv = int(round(sum( [ self.coeffs[n]*self.analogVoltage**n for n in range(len(self.coeffs)) ] )))
            #dv = int(round( numpy.polynomial.chebyshev.chebval(self.analogVoltage, self.coeffs) ))
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
        
class DACServer( LabradServer ):
    """
    CCTDAC Server
    Used for controlling DC trap electrodes
    """
    name = 'DACserver'
    serNode = 'sqip_expcontrol'
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
        degreeOfCalibration = 1 # 1st order fit. update this to auto-detect 
        #yield self.registry.cd(['', 'cctdac_pulser', 'Calibrations'])
        yield self.registry.cd(['', 'Calibrations'])
        subs, keys = yield self.registry.dir()
        sbs = ''
        for s in subs:
            sbs += s + ', '
        print 'Calibrated channels: ' + sbs 
        for i in range(1, NUMCHANNELS + 1): # Port nums are indexed from 1
            c = [] # list of calibration coefficients in form [c0, c1, ..., cn]
            if str(i) in subs:
                #yield self.registry.cd(['', 'cctdac_pulser', 'Calibrations', str(i)])
                yield self.registry.cd(['', 'Calibrations', str(i)])
                for n in range( degreeOfCalibration + 1):
                    e = yield self.registry.get( 'c'+str(n) )                    
                    c.append(e)
                self.portList.append(Port(i, c))
            else:
                self.portList.append(Port(i)) # no preset calibration
        for p in self.portList:
            p.analogVoltage = 0
            
#        yield self.registry.cd(['', 'Cfile'])
#        Cpath = yield self.registry.get('MostRecent')
#        yield self.setMultipoleControlFile(0, Cpath)
        
            
#        yield self.registry.cd(['', 'cctdac_pulser', 'Cfile'])
#        Cpath = yield self.registry.get('MostRecent')
#        yield self.setMultipoleControlFile(0, 1, Cpath)       
#        yield self.registry.cd(['', 'cctdac_pulser', 'Multipoles'])
#        ms = yield self.registry.get('Multipole Set')
#        yield self.setMultipoleVoltages(0, ms)   
        #yield self.setBigCfile(0, '/home/cct/LabRAD/cct/clients/Cfiles/A_C_extd.txt')

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
    def setAnalogVoltages( self, c, analogVoltages, setIndex = 1):
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
            if (num == 1+5):
                num = 28
            elif (num == 2+5):
                num = 27
            elif (num == 3+5):
                num = 24    
            elif (num == 4+5):
                num = 5    
            elif (num == 5+5):
                num = 20    
            elif (num == 6+5):
                num = 18   
            elif (num == 7+5):
                num = 16
            elif (num == 8+5):
                num = 13
            elif (num == 9+5):
                num = 11
            elif (num == 10+5):
                num = 1
            elif (num == 11+5):
                num = 6
            elif (num == 12+5): 
                num = 7
            elif (num == 13+5):
                num = 8
            elif (num == 14+5):
                num = 26
            elif (num == 15+5):
                num = 25
            elif (num == 16+5):
                num = 23
            elif (num == 17+5):
                num = 4
            elif (num == 18+5):
                num = 19
            elif (num == 19+5):
                num = 17
            elif (num == 20+5):
                num = 3
            elif (num == 21+5):
                num = 14
            elif (num == 22+5):
                num = 12
            elif (num == 23+5):
                num = 10            
            """
            Above if-then are hacks to bypass non-working channels on the amplifier board.  Same done on the analog voltages
            """   
                
            yield self.sendToPulser(c, [DigitalVoltage(num, dv)] )        

    @setting( 3, "Set Individual Analog Voltages", analogVoltages = '*(iv)', setIndex = 'i', returns = '')
    def setIndivAnaVoltages(self, c, analogVoltages, setIndex = 1):
        """
	    Pass a list of tuples of the form:
	    (portNum, newVolts)
	    """
        for (num, av) in analogVoltages:
            if (num == 1+5):
                num = 28
            elif (num == 2+5):
                num = 27
            elif (num == 3+5):
                num = 24    
            elif (num == 4+5):
                num = 5    
            elif (num == 5+5):
                num = 20    
            elif (num == 6+5):
                num = 18   
            elif (num == 7+5):
                num = 16
            elif (num == 8+5):
                num = 13
            elif (num == 9+5):
                num = 11
            elif (num == 10+5):
                num = 1
            elif (num == 11+5):
                num = 6
            elif (num == 12+5): 
                num = 7
            elif (num == 13+5):
                num = 8
            elif (num == 14+5):
                num = 26
            elif (num == 15+5):
                num = 25
            elif (num == 16+5):
                num = 23
            elif (num == 17+5):
                num = 4
            elif (num == 18+5):
                num = 19
            elif (num == 19+5):
                num = 17
            elif (num == 20+5):
                num = 3
            elif (num == 21+5):
                num = 14
            elif (num == 22+5):
                num = 12
            elif (num == 23+5):
                num = 10
            yield self.sendToPulser(c, [AnalogVoltage(num, av)], setIndex )

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
            print 'o'
            vectors['Ex2'] = data[:,8]            
            vectors['Ey2'] = data[:,9]
            vectors['Ez2'] = data[:,10]
            vectors['V1'] = data[:,11]
            vectors['V2'] = data[:,12]
            vectors['V3'] = data[:,13]
            vectors['V4'] = data[:,14]
            vectors['V5'] = data[:,15]
            print 'k'
            wells = 2
        except: wells = 1
        self.numWells = wells

        if index == 1:
            self.multipoleVectors1 = {}
            for key in vectors.keys():
                self.multipoleVectors1[key] = vectors[key]
            print 'new primary Cfile: ' + file
            yield self.registry.cd(['', 'cctdac_pulser', 'Cfile'])
            yield self.registry.set('MostRecent', file)                
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
        
    @setting( 12, "Shuttle Ion", position = 'i: position to move to')
    def shuttleIon(self, c, position):	
        n=1
        if position > self.curPosition:
            for i in range(self.curPosition, position):
                yield self.ShSetMultipoleVoltages(c, i + 1, n)
                n += 1
                #sleep(.1)
        elif position < self.curPosition:
            for i in range(position, self.curPosition)[::-1]:
                yield self.ShSetMultipoleVoltages(c, i, n)
                n += 1
                #sleep(.1)            
            
    @setting( 13, "Set Big Cfile", file = 's')
    def setBigCfile(self, c, file):
        import matplotlib.pyplot as plt
        data = genfromtxt(file)
        #data[0:5, 0] gives  first five entries of data's first column
        #determine width of array (num. solved positions)
        multipoles = ['Ex1', 'Ey1', 'Ez1', 'U1', 'U2', 'U3', 'U4', 'U5']
        numCols = data.size / (23 * 8)
        numPositions = numCols * 10.
        sp = {}
        spline = {}
        x = []
        for i in range(numCols): x.append(i)                      
        p = arange(0, (numCols -1) * (1 + 1/numPositions), (numCols - 1)/numPositions)
        
        n = 0
        for i in range(23):
            sp[i] = {}
            spline[i] = {}	  
            for j in multipoles:                
                sp[i][j] = UniSpline(x, data[i + n], s = 0 )                
                spline[i][j] = sp[i][j](p)                                
                n += 23                           
            n = 0
        self.spline = spline
        yield self.ShSetMultipoleVoltages(c, 0, 1)
        
        #plt.plot(x, data[23*4+1])
        #plt.show()
        #plt.plot(p, spline[1]['U2']*4.5 + .1 * spline[1]['Ex1'] + -.22*spline[1]['U1'] + .22 * spline[1]['U3'])
        #plt.show()
        
    @setting( 14, "Shuttle Set Multipole Voltages", newPosition = 'i')
    def ShSetMultipoleVoltages(self, c, newPosition, setIndex):
        multipoles = ['Ex1', 'Ey1', 'Ez1', 'U1', 'U2', 'U3', 'U4', 'U5']
        n = newPosition
        realVolts = zeros(NUMCHANNELS)
        for i in range(5):
            realVolts[i] = self.portList[i].analogVoltage  
        for i in range(23): 
            for j in multipoles:                   
                realVolts[i + 5] += self.spline[i][j][n] * self.multipoleSet[j]                      
        yield self.setAnalogVoltages(c, realVolts, setIndex)
        self.curPosition = n      
        
    @setting(15, "do nothing")
    def doNone(self, c):
        pass
                
if __name__ == "__main__":
    from labrad import util
    util.runServer( DACServer() )
