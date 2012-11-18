"""
### BEGIN NODE INFO
[info]
name = Piezo Server
version = 1.0
description = 
instancename = Piezo Server

[startup]
cmdline = %PYTHON% %FILE%
timeout = 20

[shutdown]
message = 987654321
timeout = 20
### END NODE INFO
"""

from serialdeviceserver import SerialDeviceServer, setting, inlineCallbacks, SerialDeviceError, SerialConnectionError, PortRegError
from labrad.server import Signal
from labrad.types import Error
import labrad.types as T
from twisted.internet import reactor
from twisted.internet.defer import returnValue

SIGNALID = 209068

class PS(SerialDeviceServer):
    name = 'Piezo Server'
    regKey = 'piezokey'
    serNode = 'cctmain'
    onNewUpdate = Signal(SIGNALID, 'signal: settings updated', '(sv)')
    port = None
    ret = None
    
    timeout = T.Value(.01, 's')
    baudrate = 38400
    xonxoff = False
    stopbits = 1
    bytesize = 8
    
    @inlineCallbacks
    def initServer(self):
        self.createVoltDict()
        self.createFreqDict()
        self.createCapDict()
        if not self.regKey or not self.serNode: raise SerialDeviceError( 'Must define regKey and serNode attributes' )
        #port = yield self.getPortFromReg( self.regKey )
        port = '/dev/ttyUSB1'
        self.port = port
        print  port
        try:
            serStr = yield self.findSerial(self.serNode)
            self.initSerial( serStr, port )
        except SerialConnectionError, e:
            self.ser = None
            if e.code == 0:
                print 'Could not find serial server for node: %s' % self.serNode
                print 'Please start correct serial server'
            elif e.code == 1:
                print 'Error opening serial connection'
                print 'Check set up and restart serial server'
            else: raise          
	#for i in range(100):
	    #self.ser.readline()
            
    def createFreqDict(self):
        f = {}
        f['1'] = 0
        f['2']= 0
        f['3'] = 0
        self.freqDict = f

    def createVoltDict(self):
        v = {}
        v['1'] = 0
        v['2']= 0
        v['3'] = 0
        self.voltDict = v
        
    def createCapDict(self):
        c = {}
        c['1'] = 0
        c['2']= 0
        c['3'] = 0
        self.capDict = c
                        
    @setting(1, "step", axis = 'i', numSteps = 'i', returns = '')
    def step(self, c, axis, numSteps):
        self.ser.write('setm ' + str(axis) + ' stp' + '\r\n')
        cmd = self.gtStepStr(axis, numSteps)
        self.ser.write(cmd)
        yield self.getAns(c, 'done')
	    
    @setting(2, 'continuous', axis = 'i', dirn = 's', returns = '')
    def continuous(self, c, axis, dirn):
        self.ser.write('setm ' + str(axis) + ' stp' + '\r\n')
        if dirn == 'U':
            self.ser.write('stepu ' + str(axis) + ' c\r\n')
        if dirn == 'D':
            self.ser.write('stepd ' + str(axis) + ' c\r\n')        
	
    @setting(3, "stop", axis = 'i', returns = '')
    def stop(self, c, axis):
        self.ser.write('stop ' + str(axis) + '\r\n')
        yield self.getAns(c, 'done')

    @setting(4, "sFreq", axis = 'i', freq = 'i', returns = '')
    def sFreq(self, c, axis, freq):
        self.ser.write('setf ' + str(axis) + ' ' + str(freq) + '\r\n')
        yield self.getAns(c, 'done')

    @setting(5, "sVolt", axis = 'i', volt = 'i', returns = '')
    def sVolt(self, c, axis, volt):
        self.ser.write('setv ' + str(axis) + ' ' + str(volt) + '\r\n')
        yield self.getAns(c, 'done')

    @setting(6, "gFreq", axis = 'i', returns = '')
    def gFreq(self, c, axis):
        self.ser.write('getf ' + str(axis) + '\r\n')
        yield self.getAns(c, 'f')
        freq = int(self.ret)
        self.freqDict[str(axis)] = freq
	
    @setting(7, "gVolt", axis = 'i', returns = '')
    def gVolt(self, c, axis):
        self.ser.write('getv ' + str(axis) + '\r\n')
        yield self.getAns(c, 'v')
        volt = int(self.ret)
        self.voltDict[str(axis)] = volt
	
    @setting(8, "gCap", axis = 'i', returns = '')
    def gCap(self, c, axis):
        self.ser.write('setm ' + str(axis) + ' cap' + '\r\n')
        self.ser.write('getc ' + str(axis) + '\r\n')
        yield self.getAns(c, 'c')
        cap = int(self.ret)
        self.capDict[str(axis)] = cap
	
    @setting(9, "rFreq", axis = 'i', returns = 'i')
    def rFreq(self, c, axis):
        val = self.freqDict[str(axis)]
        yield val
        returnValue(val)
	
    @setting(10, "rVolt", axis = 'i', returns = 'i')
    def rVolt(self, c, axis):
        val = self.voltDict[str(axis)]
        yield val
        returnValue(val)

    @setting(11, "rCap", axis = 'i', returns = 'i')
    def rCap(self, c, axis):
        val = self.capDict[str(axis)]
        yield val
        returnValue(val)
	
    @setting(12, "gAns", prop = 's', returns = '')
    def getAns(self, c, prop):
        listy = []
        ans = '1'
        ret = 'ERROR'
        while ans != '':
            ans = yield self.ser.readline()
            listy.append(ans)
        print listy
        for num, r in enumerate(listy):
            if r[:9] == 'frequency' and prop == 'f':
                ret = listy[num][12:-3]
            if r[:7] == 'voltage' and prop == 'v':
                ret = listy[num][10:-2]
            if r[:8] == 'capacity' and prop == 'c':
                ret = listy[num][11:-3]
        if ret != 'ERROR':
            self.ret = ret
        else:
            self.ret = 0
	  
    def gtStepStr(self, axis, numSteps):
        if numSteps >= 0:
            return 'stepu ' + str(axis)+ ' ' + str(numSteps) +  '\r\n'
        elif numSteps < 0:
            return 'stepd ' + str(axis)+ ' ' + str(-numSteps) +  '\r\n'
	  

if __name__ == "__main__":
    from labrad import util
    util.runServer(PS())
