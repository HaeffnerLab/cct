# Serial version
"""
### BEGIN NODE INFO
[info]
name = Marconi Server
version = 1.0
instancename = Marconi Server

[startup]
cmdline = %PYTHON% %FILE%
timeout = 20

[shutdown]
message = 987654321
timeout = 5
### END NODE INFO
"""

from serialdeviceserver_v1_2 import SerialDeviceServer, setting, inlineCallbacks,\
                                    SerialDeviceError, SerialConnectionError
from twisted.internet import reactor
from twisted.internet.defer import returnValue
from labrad.server import Signal
# from labrad.types import Error

SIGNALID = 209057 # what for?
SIGNALID1 = 209058

class MarconiServer(SerialDeviceServer):
    """Server for basic CW control of Marconi RF Generator"""
    
    name = 'Marconi Server'
    regKey = 'MarconiKey' # set MarconiKey in registry to /dev/ttyUSB# where # is the uSB port you are connected at
                          # actually this does not seem to work
    port = None
    serNode = 'cctmain' # name of the serial server
    timeout = 1.0
    onNewUpdate = Signal(SIGNALID, 'signal: settings updated', '(sv)') # what for?
    onStateUpdate = Signal(SIGNALID1, 'signal: state updated', 'b')
    
    @inlineCallbacks
    def initServer(self):
        self.createDict()
        if not self.regKey or not self.serNode: 
            raise SerialDeviceError('Must define regKey and serNode attributes' )
        port = yield self.getPortFromReg(self.regKey)
        self.port = port
        try:
            serStr = yield self.findSerial( self.serNode )
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
            
#         self.ser.write(self.SetAddrStr(self.gpibaddr)) # set gpib address
#         self.SetControllerWait(0) # turns off automatic listen after talk, necessary 
                                    # to stop line unterminated errors
        self.SetPowerUnits(units='DBM')
        yield self.populateDict()
        self.listeners = set()
    
    def createDict(self):
        d = {}
        d['state'] = None # state is boolean
        d['freq'] = None # frequency in MHz
        d['power'] = None # power in dBm
        self.marDict = d
    
    @inlineCallbacks
    def populateDict(self):
        state = yield self._GetState() 
        freq = yield self._GetFreq()
        power = yield self._GetPower()
        self.marDict['state'] = bool(state) 
        self.marDict['power'] = float(power)
        self.marDict['freq'] = float(freq)
        
    
    def initContext(self, c):
        """Initialize a new context object."""
        self.listeners.add(c.ID)
    
    def expireContext(self, c):
        self.listeners.remove(c.ID)
        
    def getOtherListeners(self,c):
        notified = self.listeners.copy()
        notified.remove(c.ID)
        return notified
    
    
    # SETTINGS (available to user)
    @setting(1, "Identify", returns='s')
    def Identify(self, c):
        '''Ask instrument to identify itself'''
        command = self.IdenStr()
        self.ser.write(command)
#         self.ForceRead() # expect a reply from instrument
        answer = yield self.ser.readline()
        returnValue(answer[:-1])
    
    @setting(2, "GetFreq", returns='v')
    def GetFreq(self,c):
        '''Returns current frequency (in MHz)'''
        return self.marDict['freq']

    @setting(3, "SetFreq", freq = 'v', returns = "")
    def SetFreq(self,c,freq):
        '''Sets frequency, enter value in MHZ'''
        command = self.FreqSetStr(freq)
        self.ser.write(command)
        self.marDict['freq'] = freq
        notified = self.getOtherListeners(c)
        self.onNewUpdate(('freq',freq),notified )
      
    @setting(4, "GetState", returns='b')
    def GetState(self,c):
        '''Request current on/off state of instrument'''
        return self.marDict['state']
    
    @setting(5, "SetState", state= 'b', returns = "")
    def SetState(self,c, state):
        '''Sets on/off '''
        command = self.StateSetStr(state)
        self.ser.write(command)
        self.marDict['state'] = state
        notified = self.getOtherListeners(c)
        self.onStateUpdate(state,notified)
    
    @setting(6, "GetPower", returns = 'v')
    def GetPower(self,c):
        ''' Returns current power level in dBm'''
        return self.marDict['power']
    
    @setting(7, "SetPower", level = 'v',returns = "")
    def SetPower(self,c, level):
        '''Sets power level, enter power in dBm'''
        self.checkPower(level)
        command = self.PowerSetStr(level)
        self.ser.write(command)
        self.marDict['power'] = level
        notified = self.getOtherListeners(c)
        self.onNewUpdate(('power',level),notified)
    
    @setting(8, "PowerUnits", units = 's', returns = '')
    def SetPowerUnits(self, c=None, units='dBm'):
        '''Sets power units'''
        command = self.SetPowerUnitsStr(units)
        self.ser.write(command)
        self.marDict['PwrUnits'] = units
        #notified = self.getOtherListereners(c)
        #self.onNewUpdate(('power units',units),notified)

    # HIDDEN METHODS
    @inlineCallbacks
    def ForceRead(self):
        command = self.ForceReadStr()
        yield self.ser.write(command)
    
    @inlineCallbacks
    def _GetState(self):
        command = self.StateReqStr()
        yield self.ser.write(command)
#         yield self.ForceRead() # expect a reply from instrument
        msg = yield self.ser.readline()
        state_str = msg.split(':')[2]
        if output_str == 'ENABLED':
            state = True
        else:
            state = False
        returnValue(state)
    
    @inlineCallbacks
    def _GetFreq(self):
        command = self.FreqReqStr()
        yield self.ser.write(command)
#         yield self.ForceRead() # expect a reply from instrument
        msg = yield self.ser.readline()
        freq = float(msg.split(';')[0].split()[1]) / 10**6 # freq is in MHz
        returnValue(freq)
        
    @inlineCallbacks
    def _GetPower(self):
        command = self.PowerReqStr()
        yield  self.ser.write(command)
#         yield self.ForceRead() # expect a reply from instrument
        amp = float(msg.split(';')[2].split()[1])
        answer = yield self.ser.readline()
        returnValue(answer)
    
    # STR MESSAGES
    def IdenStr(self):
        '''String to request machine to identify itself'''
        return '*IDN?'+'\n'
 
    def FreqReqStr(self):
        '''String to request current frequency'''
        return 'CFRQ?' + '\n'
        
    def FreqSetStr(self,freq):
        '''String to set freq (in MHZ)'''
        return 'CFRQ:Value ' + str(freq) + 'MHZ' + '\n'
         
    def StateReqStr(self):
        '''String to request on/off'''
        return 'OUTPUT?' + '\n'

    def StateSetStr(self, state):
        '''String to set state on/off'''
        if state:
            return 'OUTPUT:ENABLE' + '\n'
        else:
            return 'OUTPUT:DISABLE' + '\n'

    def PowerReqStr(self):
        '''String to request current power'''
        return 'RFLV?' + '\n'

    def PowerSetStr(self,pwr):
        '''String to set power (in dBm)'''
        return 'POW:AMPL ' +str(pwr) + 'DBM' + '\n'
        
    def SetPowerUnitsStr(self, units='DBM'):
        '''String to set power units (defaults to dBM)'''
        return 'RFLV:UNITS ' + units
    
    # string to force read
    def ForceReadStr(self):
        return '++read eoi' + '\n'
    
    # string to set the addressing of the prologix
    def SetAddrStr(self, addr):
        return '++addr ' + str(addr) + '\n'

__server__ = MarconiServer()

if __name__ == "__main__":
    from labrad import util
    util.runServer(__server__)