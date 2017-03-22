from qtui.QCustomFreqPower import QCustomFreqPower
from twisted.internet.defer import inlineCallbacks
from PyQt4 import QtCore, QtGui

class DDS_CHAN(QCustomFreqPower):
    def __init__(self, chan, reactor, parent=None):
        super(DDS_CHAN, self).__init__('DDS: {}'.format(chan), False, parent)
        self.reactor = reactor
        self.chan = chan
        self.connect()
        
    @inlineCallbacks
    def connect(self):
        from labrad.wrappers import connectAsync
        self.cxn = yield connectAsync()
        self.server = yield self.cxn.pulser
        yield self.server.select_dds_channel(self.chan)
        self.setupWidget()

    @inlineCallbacks
    def setupWidget(self):
        #get ranges
        MinPower,MaxPower = yield self.server.get_dds_amplitude_range()
        MinFreq,MaxFreq = yield self.server.get_dds_frequency_range()
        self.setPowerRange((MinPower,MaxPower))
        self.setFreqRange((MinFreq,MaxFreq))
        #get initial values
        initpower = yield self.server.amplitude()
        initfreq = yield self.server.frequency()
        self.spinPower.setValue(initpower)
        self.spinFreq.setValue(initfreq)
        #connect functions
        self.spinPower.valueChanged.connect(self.powerChanged)
        self.spinFreq.valueChanged.connect(self.freqChanged)
        
    @inlineCallbacks
    def powerChanged(self, pwr):
        yield self.server.amplitude(pwr)
        
    @inlineCallbacks
    def freqChanged(self, freq):
        yield self.server.frequency(freq)

    def closeEvent(self, x):
        self.reactor.stop()

class DDS_CONTROL(QtGui.QWidget):
    def __init__(self, reactor):
        super(DDS_CONTROL, self).__init__()
        self.reactor = reactor
        self.channels = ['866', '397']
        self.setupDDS()
        
    @inlineCallbacks
    def setupDDS(self):
        from labrad.wrappers import connectAsync
        self.cxn = yield connectAsync()
        self.server = yield self.cxn.pulser
        allChannels = yield self.server.get_dds_channels()
        print allChannels
        layout = QtGui.QHBoxLayout()
        for chan in self.channels:
            if chan in allChannels:
                widget = DDS_CHAN(chan, self.reactor)
                layout.addWidget(widget)
        self.setLayout(layout)
    
    def closeEvent(self, x):
        self.reactor.stop()

if __name__=="__main__":
    a = QtGui.QApplication( [] )
    import qt4reactor
    qt4reactor.install()
    from twisted.internet import reactor
    trapdriveWidget = DDS_CONTROL(reactor)

    #trapdriveWidget = RS_CONTROL_LAB(reactor)
    trapdriveWidget.show()
    reactor.run()