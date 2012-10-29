# Ryan Blais
# To Do: test, output status functionality
# Questions: where to find docs on addCallback
"""
### BEGIN NODE INFO
[info]
name = Marconi Server
version = 1.0
description = 

[startup]
cmdline = %PYTHON% %FILE%
timeout = 20

[shutdown]
message = 987654321
timeout = 5
### END NODE INFO
"""

from labrad.server import setting
from labrad.gpib import GPIBManagedServer, GPIBDeviceWarapper
from twisted.internet.defer import inlineCallbacks, returnValue

class Marconi2024Wrapper(GPIBDeviceWrapper):  
    @inlineCallbacks
    def initilize(self):
        self.frequency = yield self.getFrequency()
        self.amplitude = yield self.getAmplitude()
        self.output = yield self.getOutput()
    
    @inlineCallbacks
    def getFrequency(self):
        '''Format of frequency status message:
        :CFRQ:VALUE <nr2>;INC <nr2>;MODE<mode>
        Example:
        :CFRQ:VALUE 1000000000.0;INC 25000.0;MODE FIXED
        '''
        msg = yield self.query('CFRQ?').addCallback(str) # not sure, want string not float
        frequency = float(msg.split(';')[0].split()[1])
        self.frequency = frequency
        returnValue(self.frequency)
    
    @inlineCallbacks
    def getAmplitude(self):
        '''Format of amplitude status message:
        :RFLV:UNITS <unit>;TYPE <type>;VALUE <nr2>;INC <nr2>;<status>
        Example:
        :RFLV:UNITS DBM;TYPE PD;VALUE -103.5;INC 2.0;ON
        '''
        msg = yield self.query('RFLV?').addCallback(str) # not sure, see above
        amplitude = float(msg.split(';')[2].split()[1])
        self.amplitude = amplitude
        returnValue(self.amplitude)
    
    @inlineCallbacks
    def getOutput(self):
        '''Format of output status message:
        :OUTPUT:<status>
        Examples:
        :OUTPUT:ENABLE
        :OUTPUT:DISABLE
        '''
        # This is not very elegant, if it does not work it's 
        # likely a problem with the formatting.
        msg = yield self.query('OUTPUT?').addCallback(str) # not sure, see above
        output = msg.split(':')[2]
        self.output = output
        returnValue(self.output)
        
    @inlineCallbacks
    def setFrequency(self, f):
        if self.frequency != f:
            yield self.write('CFRQ:Value {}'.format(float(f)))
            self.frequency = f
    
    @inlineCallbacks
    def setAmplitude(self, a):
        if self.amplitude != a:
            yield self.write('RFLV:Value {}'.format(float(a)))
            self.amplitude = a
    
    @inlineCallbacks
    def setOutput(self, o):
        if self.output != o:
            yield self.write('OUTPUT:' + '{}'.format(o))
            self.output = o


class MarconiServer(GPIBManagedServer):
    """Provides basic CW control for Marconi 2024 RF Generators"""
    name = 'Marconi Server'
    deviceName = 'IFR,2024,112236/043,44533/466/03.04'
    deviceWrapper = Marconi2024Wrapper
    
    @setting(10, 'Frequency', f=['v[MHz]'], returns=['v[MHz]'])
    def frequency(self, c, f=None):
        """Get or set the CW frequency."""
        dev = self.selectedDevice(c)
        if f is not None:
            yield dev.setFrequency(f)
        returnValue(dev.frequency)
    
    @setting(11, 'Amplitude', a=['v[dBm]'], returns=['v[dBm]'])
    def amplitude(self, c, a=None):
        """Get or set the CW amplitude."""
        dev = self.selectedDevice(c)
        if a is not None:
            yield dev.setAmplitude(a)
        returnValue(dev.amplitude)

#     @setting(12, 'Output', os=['b'], returns=['b'])
#     def output_state(self, c, os=None): 
#         """Get or set the output status."""
#         dev = self.selectedDevice(c)
#         if os is not None:
#             yield dev.setFrequency(os)
#             yield dev.setAmplitude(os)
#         returnValue(dev.output)

    @setting(13, 'OnOff', state = 'b', returns = 'b')
    def on_off(self, c, state):
        dev = self.selectedDevice(c)
        if state is not None:
            yield dev.setOutput(state)
        returnValue(dev.output)
        
__server__ = MarconiServer()

if __name__ == '__main__':
    test = 0
    if not test:
        print 'Marconi server has not been tested'
    else:        
        from labrad import util
        util.runServer(__server__)
        s = __server__
        print 'Frequency = ' + str(s.frequency)
        print 'Amplitude = ' + str(s.amplitude)
        print 'Output State = ' + s.output