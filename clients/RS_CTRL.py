import os
from PyQt4 import QtGui
from PyQt4 import QtCore,uic
from twisted.internet.defer import inlineCallbacks, returnValue

MinPower = -36 #dbM
MaxPower = 0
DEFPower = -20
MinFreq = 0 #Mhz
MaxFreq = 20
DEFFreq = 10

class RS(QtGui.QWidget):
    def __init__(self, reactor, parent=None):
        super(RS,self).__init__(parent)
        self.reactor = reactor
        self.connect()
        
        layout = QtGui.QGridLayout()
        subLayout = QtGui.QGridLayout()
        superLayout = QtGui.QGridLayout()
        
        self.powerCtrl = QtGui.QDoubleSpinBox()
        self.powerCtrl.setRange (MinPower,MaxPower)
        self.powerCtrl.setDecimals (2)
        self.frequencyCtrl = QtGui.QDoubleSpinBox()
        self.frequencyCtrl.setRange (MinFreq,MaxFreq)
        self.frequencyCtrl.setDecimals (5)
        self.frequencyCtrl.setSingleStep(10**-4) 
        self.stateButton = QtGui.QPushButton()
        
        superLayout.addLayout(layout,0,0)
        layout.addLayout(subLayout,1,0)
        subLayout.addWidget(QtGui.QLabel('Frequency'),0,0) 
        subLayout.addWidget(self.frequencyCtrl,0,1)
        subLayout.addWidget(QtGui.QLabel('Power'),1,0) 
        subLayout.addWidget(self.powerCtrl,1,1)
        layout.addWidget(self.stateButton,0,0)

        self.setLayout(superLayout)
    
    @inlineCallbacks
    def connect(self):
        from labrad.wrappers import connectAsync
        from labrad.types import Error
        self.cxn = yield connectAsync('192.168.169.30')
        self.server = yield self.cxn.rohdeschwarz_server
        try:
            yield self.server.select_device('GPIB Bus - USB0::0x0AAD::0x0054::102542')
        except Error:
            self.setEnabled(False)
            return
        #set initial values
        initpower = yield self.server.amplitude()
        initfreq = yield self.server.frequency()
        initstate = yield self.server.output()
        #set properties
#        self.frequencyCtrl.setDecimals(5)
#        self.frequencyCtrl.setSingleStep(10**-4) #set step size to 100HZ
        self.powerCtrl.setValue(initpower)
        self.frequencyCtrl.setValue(initfreq)
        self.stateButton.setChecked(initstate)
        if initstate:
            self.stateButton.setText('Rohde&Schwarz: ON')
        else:
            self.stateButton.setText('Rohde&Schwarz: OFF')
            
        self.state = initstate
        #connect functions
        self.powerCtrl.valueChanged.connect(self.onPowerChange)
        self.frequencyCtrl.valueChanged.connect(self.onFreqChange)
        self.stateButton.clicked.connect(self.onOutputChange)
    
    @inlineCallbacks
    def onOutputChange(self, state):
        if self.state:
            self.stateButton.setText('Rohde&Schwarz: OFF')
            yield self.server.onoff(False)
        if not self.state:
            self.stateButton.setText('Rohde&Schwarz: ON')
            yield self.server.onoff(True)
        self.state = not self.state
        
    @inlineCallbacks
    def onFreqChange(self, f):
        yield self.server.frequency(self.frequencyCtrl.value())

    @inlineCallbacks
    def onPowerChange(self, p):
        yield self.server.amplitude(self.powerCtrl.value())
    
    def closeEvent(self, x):
        self.reactor.stop()

class RS_CONTROL(QtGui.QMainWindow):
    def __init__(self, reactor, parent=None):
        super(RS_CONTROL, self).__init__(parent)
        self.reactor = reactor
        W = self.buildW(reactor)
        widget = QtGui.QWidget()
        gridLayout = QtGui.QGridLayout()    
#        gridLayout.addWidget(RS(reactor), 1, 0)
        gridLayout.addWidget(W, 1, 0)
        self.setWindowTitle('RS Control')
        widget.setLayout(gridLayout) 
        self.setCentralWidget(widget)

    def buildW(self, reactor):
        
        W = QtGui.QWidget()
        subLayout = QtGui.QGridLayout()
        subLayout.addWidget(RS(reactor), 1, 0)
        W.setLayout(subLayout)
        return W
                
    def closeEvent(self, x):
        self.reactor.stop()
        
if __name__=="__main__":
    a = QtGui.QApplication( [] )
    import qt4reactor
    qt4reactor.install()
    from twisted.internet import reactor
    RS_CONTROL = RS_CONTROL(reactor)
    RS_CONTROL.show()
    reactor.run()
