from PyQt4 import QtGui
from PyQt4 import QtCore,uic
from twisted.internet.defer import inlineCallbacks, returnValue

class SHUTTER (QtGui.QWidget):
    """
    assumes manualinversion in pulser's hardwareConfiguration.py is set to False for each laser
    """
    def __init__(self, reactor, parent=None):
        super(SHUTTER, self).__init__(parent)
        print 'here'
        self.reactor = reactor
        self.channels = ['375sw']        
        self.makeGUI()
        self.connect()
        
    def makeGUI(self):            
        layout = QtGui.QGridLayout()
        self.setLayout(layout)
        groupBox = QtGui.QGroupBox('Shutters')
        groupBoxLayout = QtGui.QVBoxLayout()
        self.button = {}
        for channel in self.channels:
            self.button[channel] = QtGui.QPushButton()
            groupBoxLayout.addWidget(self.button[channel])
            self.button[channel].clicked.connect(self.switch(channel))
        groupBox.setLayout(groupBoxLayout)
        layout.addWidget(groupBox)

    @inlineCallbacks
    def connect(self):
        from labrad.wrappers import connectAsync
        cxn = yield connectAsync()
        self.pulser = cxn.pulser
        for channel in self.channels:
            stateTuple = yield self.pulser.get_state(channel)
            if stateTuple[0]:
                if stateTuple[1]: self.button[channel].setText(self.name(channel) + ': Open')
                else: self.button[channel].setText(self.name(channel) + ': Closed')
            else: 
                if stateTuple[3]: self.button[channel].setText(self.name(channel) + ': Open (Auto)')
                else: self.button[channel].setText(self.name(channel) + ': Closed (Auto)') 
           
    def switch(self, channel):
        @inlineCallbacks 
        def fn(something):
            stateTuple = yield self.pulser.get_state(channel)
            if stateTuple[0]: 
                if stateTuple[1] != stateTuple[3]:
                    self.pulser.switch_auto(channel)
                    if stateTuple[3]: self.button[channel].setText(self.name(channel) + ': Open (Auto)')
                    else: self.button[channel].setText(self.name(channel) + ': Closed (Auto)')
                else:
                    self.pulser.switch_manual(channel, not stateTuple[1])
                    if stateTuple[1]: self.button[channel].setText(self.name(channel) + ': Closed')
                    else: self.button[channel].setText(self.name(channel) + ': Open')
            else:
                self.pulser.switch_manual(channel, not stateTuple[3])
                if stateTuple[3]: self.button[channel].setText(self.name(channel) + ': Closed')
                else: self.button[channel].setText(self.name(channel) + ': Open')
        return fn

    def name(self, channel):
        if channel == '375sw': return '375sw'
        else: return channel
        
class SHUTTER_CONTROL(QtGui.QMainWindow):
    def __init__(self, reactor, parent=None):
        super(SHUTTER_CONTROL, self).__init__(parent)
        self.reactor = reactor
        widget = QtGui.QWidget()
        gridLayout = QtGui.QGridLayout()    
        gridLayout.addWidget(SHUTTER(reactor), 0, 0)        
        widget.setLayout(gridLayout) 
        self.setCentralWidget(widget) 
        self.setWindowTitle('Shutter Control')
                
    def closeEvent(self, x):
        self.reactor.stop()

if __name__=="__main__":
    a = QtGui.QApplication( [] )
    import qt4reactor
    qt4reactor.install()
    from twisted.internet import reactor
    SHUTTER_CONTROL = SHUTTER_CONTROL(reactor)
    SHUTTER_CONTROL.show()
    reactor.run()