# Control for table optics

from PyQt4 import QtGui, QtCore, uic
from qtui.SliderSpin import SliderSpin
from twisted.internet.defer import inlineCallbacks, returnValue

UpdateTime = 100 # ms
SIGNALID = 27883

class widgetWrapper():
    def __init__(self, displayName, freqRange):
        self.widget = None
        self.range = freqRange
        self.updated = False
        self.displayName = displayName
        self.freqRange = freqRange

    def makeWidget(self):
        self.widget = SliderSpin(self.displayName, 'MHz', self.freqRange, self.freqRange)

    def onUpdate(self):
        self.updated = True

class OPTICS_CONTROL(QtGui.QWidget):
    def __init__(self, reactor, parent=None):
        super(OPTICS_CONTROL, self).__init__(parent)

        self.reactor = reactor
        self.createDict()
        self.connect()
        
    def createDict(self):
        self.d = {}
        self.d['397DP'] = widgetWrapper( displayName = '397DP', freqRange = (150, 300) )
        self.d['866DP'] = widgetWrapper( displayName = '866DP', freqRange = (60, 150) )
        self.d['854DP'] = widgetWrapper( displayName = '854DP', freqRange = (60, 150) )
        
    @inlineCallbacks
    def connect(self):
        from labrad.wrappers import connectAsync
        from labrad.types import Error
        self.cxn = yield connectAsync()
        self.server = yield self.cxn.vcoserver
        yield self.loadDict()
        yield self.setupListeners()
        yield self.initializeGUI()

    @inlineCallbacks
    def loadDict(self):
        for wrapper in self.d.values():
            wrapper.makeWidget()
        yield None
    
    @inlineCallbacks
    def setupListeners(self):
        yield self.server.signal__vcos_updated
        yield self.server.addListener(listener = self.followSignal, source = None, ID = SIGNALID)

    def followSignal(self, x, (chanName, freq) ):
        widget = self.d[chanName].widget
        widget.setValueNoSignal(freq)

    def sizeHint(self):
        return QtCore.QSize(400, 200)

    @inlineCallbacks
    def initializeGUI(self):
        yield None
        layout = QtGui.QVBoxLayout()
        self.setLayout(layout)
        
        for wrapper in self.d.values():
            wrapper.widget.spin.setValue ( wrapper.freqRange[0] )
            layout.addWidget( wrapper.widget )
            wrapper.widget.spin.valueChanged.connect(wrapper.onUpdate)

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.sendToServer)
        self.timer.start(UpdateTime)
    
    @inlineCallbacks
    def sendToServer(self):
        import labrad.types as T
        for wrapper in self.d.values():
            if wrapper.updated:
                f = T.Value( wrapper.widget.spin.value(), 'MHz' )
                yield self.server.set_frequency( wrapper.displayName, f)
                wrapper.updated = False

    def closeEvent(self, x):
        self.reactor.stop()

if __name__ == "__main__":
    a = QtGui.QApplication( [] )
    import qt4reactor
    qt4reactor.install()
    from twisted.internet import reactor
    control = OPTICS_CONTROL( reactor )
    control.show()
    reactor.run()
