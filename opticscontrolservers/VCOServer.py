"""
### BEGIN NODE INFO
[info]
name = VCOServer
version = 1.0
description = 
instancename = VCOServer

[startup]
cmdline = %PYTHON% %FILE%
timeout = 20

[shutdown]
message = 987654321
timeout = 20
### END NODE INFO
"""



from labrad.server import LabradServer, setting, Signal
from twisted.internet.defer import Deferred, returnValue, inlineCallbacks

SIGNALID = 331500

class VCOServer( LabradServer ):

    name = "VCOServer"
    registryDirectory = ['', 'Servers', 'VCO']
    onNewUpdate = Signal(SIGNALID, 'signal: vcos updated', 's')
    
    @inlineCallbacks
    def initServer(self):

        self.listeners = set()
        yield self.setupDictionary()

    @inlineCallbacks
    def setupDictionary(self):
        self.channels = ['854DP', '866DP', '397DP']

        self.calibDict = {}
        self.freqDict = {}
        self.inversionDict = {}
        self.dacChannelDict = {}
        self.calibDict = {}
        for c in self.channels:
            self.inversionDict[c] = yield self.lookupInversion(c)
            self.freqDict[c] = yield self.lookupFrequencyRange(c)
            self.dacChannelDict[c] = yield self.lookupDacChannel(c)
            self.calibDict[c] = yield self.lookupFrequencyCalibration(c)

    @inlineCallbacks
    def lookupInversion(self, channel):
        """ Returns the value needed to turn light on """
        regDir = self.registryDirectory + [channel]
        yield self.client.registry.cd(regDir)
        light_on_setting = yield self.client.registry.get('light_on_setting')
        returnValue(light_on_setting)

    @inlineCallbacks
    def lookupFrequencyRange(self, channel):
        regDir = self.registryDirectory + [channel]
        yield self.client.registry.cd(regDir)    
        frequency_range = yield self.client.registry.get('frequency_range')
        returnValue(frequency_range)

    @inlineCallbacks
    def lookupDacChannel(self, channel):
        regDir = self.registryDirectory + [channel]
        yield self.client.registry.cd(regDir)
        dac_channel_number = yield self.client.registry.get('dac_channel')
        returnValue(dac_channel_number)

    @inlineCallbacks
    def lookupFrequencyCalibration(self, channel):
        import labrad.types as T
        regDir = self.registryDirectory + [channel, 'calibration']
        yield self.client.registry.cd(regDir)
        c0 = yield self.client.registry.get('c0')
        c1 = yield self.client.registry.get('c1')
        try:
            c2 = yield self.client.registry.get('c2')
            c3 = yield self.client.registry.get('c3')
        except:
            c2 = T.Value(0.0, '1/MHz^2')
            c3 = T.Value(0.0, '1/MHz^3')
        print c2
        calibration = [c0, c1, c2, c3]
        returnValue(calibration)
    
    @inlineCallbacks
    def freqToVoltage(self, channel, freq):
        yield None
        calib = self.calibDict[channel]
        voltage = sum ([ calib[n]*freq**n for n in range(len(calib)) ])
        returnValue(voltage)

    @inlineCallbacks
    def setFrequency(self, channel, freq):
        voltage = yield self.freqToVoltage(channel, freq)
        channelNum = self.dacChannelDict[channel]
        print voltage
        yield self.client.cctdac_serial.set_individual_digital_voltages( [(channelNum, voltage) ])

    def initContext(self, c):
        """ Initialize a new context object """

        self.listeners.add(c.ID)

    def expireContext(self, c):
        self.listeners.remove(c.ID)

    def getOtherListeners(self, c):
        notified = self.listeners.copy()
        notified.remove(c.ID)
        return notified


    @setting(0, "Init all off", returns = '')
    def initAllLasersOff(self, c):
        '''
        Program the pulser such that the auto state turns the light off.
        Probably the default for most experiments.
        '''

        for chan in self.channels:
            light_on_val = self.inversionDict[chan]
            yield self.client.pulser.switch_auto( chan,  light_on_val )

    @setting(1, "Switch all off", returns = '')
    def switchAllLasersOff(self, c):
        for chan in self.channels:
            light_on_val = self.inversionDict[chan]
            yield self.client.pulser.switch_manual( chan,  not light_on_val )

    @setting(2, "Switch off", chan = '*s', returns = '')
    def switchLaserOff(self, c, chan):
        chan = ''.join(chan)
        light_on_val = self.inversionDict[chan]
        yield self.client.pulser.switch_manual( chan,  not light_on_val )

    @setting(3, "Switch on", chan = '*s', returns = '')
    def switchLaserOn(self, c, chan):
        chan = ''.join(chan)
        light_on_val = self.inversionDict[chan]
        yield self.client.pulser.switch_manual( chan, light_on_val )

    @setting(4, "Set frequency", chan='*s', freq = 'v[MHz]', returns = '')
    def setVCOFrequency(self, c, chan, freq):
        chan = ''.join(chan)
        notified = self.getOtherListeners(c)
        self.onNewUpdate('VCOs updated', notified)
        yield self.setFrequency(chan, freq)        

if __name__ == "__main__":
    from labrad import util
    util.runServer(VCOServer())
