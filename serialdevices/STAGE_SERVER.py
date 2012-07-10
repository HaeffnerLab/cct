"""
### BEGIN NODE INFO
[info]
name = Stage Server
version = 1.0
description = 
instancename = %LABRADNODE% Stage Server

[startup]
cmdline = %PYTHON% %FILE%
timeout = 20

[shutdown]
message = 987654321
timeout = 20
### END NODE INFO
"""

from serialdeviceserver import SerialDeviceServer, setting, inlineCallbacks, SerialDeviceError, SerialConnectionError, PortRegError
from labrad.types import Error
from twisted.internet import reactor
from twisted.internet.defer import returnValue
from labrad.server import Signal
import time

SIGNALID = 209068

class STS(SerialDeviceServer):
    name = '%LABRADNODE% Stage Server'
    regKey = 'sskey'
    port = None
    serNode = 'cctmain'
    timeout = 1.0
    baudrate = 57600
    xonxoff = True
    onNewUpdate = Signal(SIGNALID, 'signal: settings updated', '(sv)')
    defaultState = '32'
    
    @inlineCallbacks
    def initServer(self):
        self.createStateDict()
        self.createDict()
        if not self.regKey or not self.serNode: raise SerialDeviceError( 'Must define regKey and serNode attributes' )
        port = yield self.getPortFromReg( self.regKey )
        self.port = port
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
        
        for i in range(1, 5):
            self.ser.write(str(i) + 'OR\r\n')
                
    def createDict(self):
        d = {}
        d['x1displacement'] = 0
        d['y1displacement']= 0
        d['x2displacement'] = 0
        d['y2displacement']= 0
        self.sstDict = d
        
        
    def createStateDict(self):
        d = {}
        d['x1state'] = 0
        d['y1state']= 0
        d['x2state'] = 0
        d['y2state']= 0
        self.stateDict = d
                
    @setting(1, "move abs", label = 's', absDisp = 'v', returns = '')
    def mvAbs(self, c, label, absDisp):
        cmd = self.mvAbsStr(label, absDisp)
        self.ser.write(cmd)
            
    @setting(2, "ask state", label = 's', returns = '')
    def askState(self, c, label):
        cmd = self.gtStateStr(label)
        yield self.ser.write(cmd)
        state = yield self.ser.readline()  #controller returns '(nn)(TP)[disp]\r\n'
        if state != None:
            state = state[7] + state[8]
            state = int(state)
            if state == 32:
                ready = 1
            elif state == 33:
                ready = 1
            elif state == 34:
                ready = 1
            elif state == 35:
                ready = 1    
            elif state == 28:
                ready = 0
            else: ready = 0
            self.stateDict[label + 'displacement'] = ready
            
    @setting(3, "get state", label = 's', returns = 'i')
    def getState(self,c, label):
        ready = self.stateDict[label + 'displacement']
        yield ready
        returnValue(ready)
    

    def labelToNum(self, label):
        if label == 'x1':
            return '1'    
        if label == 'y1':
            return '2'
        if label == 'x2':
            return '3'    
        if label == 'y2':
            return '4'   
        else:
            return '5'

    def gtStateStr(self, label):
        return self.labelToNum(label) + 'TS\r\n'
     
    def gtDispStr(self, label):
        return self.labelToNum(label) + 'TP?\r\n'
    
    def mvAbsStr(self, label, netDisp):
        return self.labelToNum(label) + 'PA' + str(netDisp) + '\r\n'

if __name__ == "__main__":
    from labrad import util
    util.runServer(STS())
