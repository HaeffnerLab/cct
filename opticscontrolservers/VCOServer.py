### Server for controlling VCO's

from labrad.server import LabradServer, setting, Signal
from twisted.internet.defer import Deferred, returnValue, inlineCallbacks

SIGNALID = 331500

class VCOServer( LabradServer ):

    registryDirectory = ['', 'Servers', 'VCO']
    
    @inlineCallbacks
    def initServer(self):

        self.listeners = set()
        yield self.setupDictionary()

    @inlineCallbacks
    def setupDictionary(self):
        self.channels = ['854DP', '397DP', '866DP']

        self.calibDict = {}
        self.freqDict = {}
        self.inversionDict = {}
        self.dacChannelDict = {}
        self.calibDict = {}
        for c in channels:
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
    def lookupFrequencyCalibration(self, channel)
        regDir = self.registryDirectory + [channel, 'calibration']
        yield self.client.registry.cd(regDir)
        calibration = yield self.client.registry.get('calib')
        returnValue(calibration)

    @inlineCallbakcs
    def freqToVoltage(self, channel, freq):
        calib = self.calibDict[channel]
        voltage = sum([ calib[n] * v**n for n in range(len(calib)) ])
        returnValue(voltage)

    @inlineCallbacks
    def setFrequency(self, channel, freq):
        voltage = yield freqToVoltage(freq).Value()
        channelNum = dacChannelDict[channel].Value()

        yield self.client.cctdac.set_individual_analog_voltages( (channelNum, voltage) )
        

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
            yield self.client.pulser.switch_auto( chan,  not light_on_val )

    @setting(1, "Switch all off", returns = '')
    def switchAllLasersOff(self, c):
        for chan in self.channels:
            light_on_val = self.inversionDict[chan]
            yield self.client.pulser.switch_manual( chan,  not light_on_val )

    @setting(2, "Switch off", chan = '*s', returns = '')
    def switchLaserOff(self, c, chan):
        light_on_val = self.inversionDict[chan]
        yield self.client.pulser.switch_manual( chan,  not light_on_val )

    @setting(3, "Set frequency", chan='*s', freq = '*v', returns = '')
    def setVCOFrequency(self, c, chan, freq):
        yield self.setFrequency(chan, freq)
        
