"""
### BEGIN NODE INFO
[info]
name = Advantest Server
version = 1.0
description =
instancename = Advantest Server

[startup]
cmdline = %PYTHON% %FILE%
timeout = 20

[shutdown]
message = 987654321
timeout = 20
### END NODE INFO
"""

from serialdeviceserver import SerialDeviceServer, setting, inlineCallbacks, SerialDeviceError, SerialConnectionError
from labrad.server import Signal
import labrad.types as T
from twisted.internet import reactor
from twisted.internet.defer import returnValue

SIGNALID = 207631

class PS(SerialDeviceServer):
    name = 'Advantest Server'
    serNode = 'cctmain'
    onNewUpdate = Signal(SIGNALID, 'signal: settings updated', '(sv)')
    port = '/dev/ttyUSB0'
    timeout = T.Value(.01, 's')
    
    @inlineCallbacks
    def initServer(self):
        port = self.port
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
        yield self.ser.write('++addr1\r\n')
                        
    @setting(1, "get peak info", returns = 'v[Hz]v[dBm]')
    def step(self, c):
        self.ser.write('MFL?\r\n')
        ans = ''
        while ans == '':
            ans = yield self.ser.readline()
        freq = T.Value(float(ans.split(',')[0]), 'Hz')
        amp = T.Value(float(ans.split(',')[1]), 'dBm')
        returnValue([freq, amp])

    """ untested functions """
    @setting(2, "TraceReq", filename = 's')
    def TraceReq(self, c, filename):
        command = self.TraceReqStr()
        self.ser.write(command)
        f = open(filename, 'a')
        k = yield(self.ser.read(10020))
        f.write(k)    

    #1 is 16  bit integer, 3 is 32 bit ieee float
    @setting(3, "SetTraceFormat", format = 'i', returns = '')
    def SetTraceFormat(self, c,  format):      
        if format!=1 and format!=3:
                print "Format must be 1 or 3"
                return
        command = self.SetTraceFormatStr(format)
        self.ser.write(command)

    @setting(4, "SelectedTraceQuery", returns = 'i')
    def SelectedTraceQuery(self,c):
        self.ser.write("TRACESEL?\r")
        self.ForceRead()
        answer = self.ser.read_line()
        return answer

    @inlineCallbacks
    def ForceRead(self):
       command = self.ForceReadStr()
       yield self.ser.write(command)

    def TraceReqStr(self):
        return 'TAA?' + '\n'

    def SetTraceFormatStr(self, format):
        return 'FORM' + str(format) + '\n'

    # string to force read
    def ForceReadStr(self):
        return '++read eoi' + '\n'

    # string for prologix to request a response from instrument, wait can be 0 for listen / for talk
    def WaitRespStr(self, wait):
        return '++auto '+ str(wait) + '\n'

if __name__ == "__main__":
    from labrad import util
    util.runServer(PS())
