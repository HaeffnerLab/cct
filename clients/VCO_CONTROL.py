'''
Client for controlling voltage-controlled oscillators.

Dylan Gorman
'''

from PyQt4 import QtGui, QtCore, uic
from qtui.SliderSpin import SliderSpin
from twisted.internet.defer import inlineCallbacks, returnValue


UpdateTime = 100 # ms
SIGNALID = 27882

class Calibration():
    def __init__(self, f0, dvdf):
        from labrad import types as T
        self.T = T
        self.f0 = f0
        self.dvdf = dvdf
        self.v0 = -(dvdf)*f0

    def getVoltage(self, f):
        ''' v = f0 + (dvdf)f '''
        return self.T.Value(self.v0 + (self.dvdf)*f, 'V')

    def getFrequency(self, v):
        return self.T.Value((v - self.f0)/(self.dvdf), 'MHz')
        

class widgetWrapper():
    def __init__(self, displayName, freqRange, voltRange, dacChannel, calibration = None):
        from labrad import types as T
        self.T = T
        self.displayName = displayName
        self.freqRange = freqRange
        self.voltRange = voltRange
        self.dacChannel = dacChannel
        self.range = None
        self.widget = None
        self.updated = False
        print freqRange

        if calibration is None:
            self.calibration = Calibration( freqRange[0], (voltRange[1] - voltRange[0])/(freqRange[1] - freqRange[0]) )

    def getVoltage(self, f):
        return self.calibration.getVoltage(f)
        
    def getFrequency(self, v):
        return self.calibration.getFrequency(v)

    def makeWidget(self):
        self.widget = SliderSpin(self.displayName, 'MHz', self.freqRange, self.freqRange)

    def onUpdate(self):
        self.updated = True

class VCO_CONTROL(QtGui.QWidget):
    def __init__(self, reactor, parent=None):
        super(VCO_CONTROL, self).__init__(parent)
        self.reactor = reactor
        self.createDict()
        self.connect()

    def createDict(self):
        self.d = {}
        self.d['397'] = widgetWrapper( displayName = '397', dacChannel = 1, freqRange = (200, 240), voltRange = (0, 2.5) )
        self.d['866'] = widgetWrapper( displayName = '866', dacChannel = 2, freqRange = (60, 100), voltRange = (0, 2.5) )

    @inlineCallbacks
    def connect(self):
        from labrad.wrappers import connectAsync
        from labrad.types import Error
        self.cxn = yield connectAsync()
        self.server = yield self.cxn.cctdac
        self.registry = yield self.cxn.registry
        yield self.loadDict()
        yield self.setupListeners()
        yield self.initializeGUI()
    
    @inlineCallbacks
    def loadDict(self):
        for w in self.d.values():
            w.makeWidget()
        yield None

    @inlineCallbacks
    def setupListeners(self):
        yield self.server.signal__ports_updated(SIGNALID)
        yield self.server.addListener(listener = self.followSignal, source = None, ID = SIGNALID)

    def followSignal(self, x, (chanName, freq)):
        widget = self.d[chanName].widget
        widget.setValueNoSignal(freq)

    def sizeHint(self):
        return QtCore.QSize(400,200)

    @inlineCallbacks
    def initializeGUI(self):
        voltageList = yield self.server.get_analog_voltages()
        for chanName in self.d.keys():
            n = self.d[chanName].dacChannel
            v0 = voltageList[n]
            f0 = self.d[chanName].getFrequency( v0 )
            self.d[chanName].widget.spin.setValue( f0.value )

        # lay out the widget
        layout = QtGui.QVBoxLayout()
        self.setLayout(layout)
        for name in ['397', '866']:
            layout.addWidget(self.d[name].widget)
        for widgetWrapper in self.d.values():
            widgetWrapper.widget.spin.valueChanged.connect(widgetWrapper.onUpdate)

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.sendToServer)
        self.timer.start(UpdateTime)

    @inlineCallbacks
    def sendToServer(self):
        for widgetWrapper in self.d.values():
            if widgetWrapper.updated:
                dacChannel = widgetWrapper.dacChannel
                f = widgetWrapper.widget.spin.value()
                v = widgetWrapper.getVoltage(f)
                print dacChannel
                print v
                yield self.server.set_individual_analog_voltages([(dacChannel, v)])
                widgetWrapper.updated = False

    def closeEvent(self, x):
        self.reactor.stop()

if __name__=="__main__":
    a = QtGui.QApplication( [] )
    import qt4reactor
    qt4reactor.install()
    from twisted.internet import reactor
    VCO_CONTROL = VCO_CONTROL(reactor)
    VCO_CONTROL.show()
    reactor.run()



