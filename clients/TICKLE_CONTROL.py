import os
from PyQt4 import QtGui
from PyQt4 import QtCore,uic
from twisted.internet.defer import inlineCallbacks, returnValue

MinPower = -100 #dbM
MaxPower = 0
MinFreq = 0 #Mhz
MaxFreq = 100


class T(QtGui.QWidget):
    def __init__(self, reactor, parent=None):
        super(T,self).__init__(parent)
        self.reactor = reactor
        self.connect()
        
        layout = QtGui.QGridLayout()
        subLayout = QtGui.QGridLayout()
        superLayout = QtGui.QGridLayout()
        groupbox = QtGui.QGroupBox('Tickle')
        groupboxLayout = QtGui.QGridLayout()
        self.powerCtrl = QtGui.QDoubleSpinBox()
        self.powerCtrl.setRange (MinPower,MaxPower)
        self.powerCtrl.setDecimals (2)
        self.powerCtrl.setSingleStep(.5)
        self.powerCtrl.setSuffix(' dBm')
        self.frequencyCtrl = QtGui.QDoubleSpinBox()
        self.frequencyCtrl.setRange (MinFreq,MaxFreq)
        self.frequencyCtrl.setDecimals (5)
        self.frequencyCtrl.setSingleStep(.1)
        self.frequencyCtrl.setSuffix(' MHz')
        self.updateButton = QtGui.QPushButton('Update')
        self.stateButton = QtGui.QPushButton()
        
        superLayout.addLayout(layout,0,0)
        groupbox.setLayout(groupboxLayout)
        layout.addWidget(groupbox,0,0)
        groupboxLayout.addWidget(QtGui.QLabel('Frequency'),1,0) 
        groupboxLayout.addWidget(self.frequencyCtrl,1,1)
        groupboxLayout.addWidget(QtGui.QLabel('Power'),2,0) 
        groupboxLayout.addWidget(self.powerCtrl,2,1)
        groupboxLayout.addWidget(self.stateButton,0,0,1,1)
        groupboxLayout.addWidget(self.updateButton,0,1,1,1)

        self.setLayout(superLayout)
    
    @inlineCallbacks
    def connect(self):
        from labrad.wrappers import connectAsync
        from labrad.types import Error
        self.cxn = yield connectAsync('192.168.169.30')
        self.server = yield self.cxn.rohdeschwarz_server
        try:
            yield self.server.select_device('GPIB Bus - USB0::0x0AAD::0x0054::104543')
        except Error:
            self.setEnabled(False)
            return
        self.update(0)
        #set initial values
        #initpower = yield self.server.amplitude()
        #initfreq = yield self.server.frequency()
        #initstate = yield self.server.output()
        ##set properties
##        self.frequencyCtrl.setDecimals(5)
##        self.frequencyCtrl.setSingleStep(10**-4) #set step size to 100HZ
        #self.powerCtrl.setValue(initpower)
        #self.frequencyCtrl.setValue(initfreq)
        #self.stateButton.setChecked(initstate)
        #if initstate:
            #self.stateButton.setText('Rohde&Schwarz: ON')
        #else:
            #self.stateButton.setText('Rohde&Schwarz: OFF')
            
        #self.state = initstate
        #connect functions
        self.powerCtrl.valueChanged.connect(self.onPowerChange)
        self.frequencyCtrl.valueChanged.connect(self.onFreqChange)
        self.stateButton.clicked.connect(self.onOutputChange)
        self.updateButton.clicked.connect(self.update)
    
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
    def update(self, c):
        currentpower = yield self.server.amplitude()
        currentfreq = yield self.server.frequency()
        currentstate = yield self.server.onoff()
        self.powerCtrl.setValue(currentpower)
        self.frequencyCtrl.setValue(currentfreq)
        if currentstate:
            self.stateButton.setText('Rohde&Schwarz: ON')
        else:
            self.stateButton.setText('Rohde&Schwarz: OFF')
            
        self.state = currentstate
	
        
    @inlineCallbacks
    def onFreqChange(self, f):
        yield self.server.frequency(self.frequencyCtrl.value())

    @inlineCallbacks
    def onPowerChange(self, p):
        yield self.server.amplitude(self.powerCtrl.value())

    
    def closeEvent(self, x):
        self.reactor.stop()

class Tickle_Control(QtGui.QMainWindow):
    def __init__(self, reactor, parent=None):
        super(Tickle_Control, self).__init__(parent)
        self.reactor = reactor
        W = self.buildW(reactor)
        widget = QtGui.QWidget()
        gridLayout = QtGui.QGridLayout()    
        gridLayout.addWidget(W, 1, 0)
        self.setWindowTitle('Tickle Control')
        widget.setLayout(gridLayout) 
        self.setCentralWidget(widget)

    def buildW(self, reactor):
        
        W = QtGui.QWidget()
        subLayout = QtGui.QGridLayout()
        subLayout.addWidget(T(reactor), 0, 0)
        W.setLayout(subLayout)
        return W
                
    def closeEvent(self, x):
        self.reactor.stop()
        
if __name__=="__main__":
    a = QtGui.QApplication( [] )
    import qt4reactor
    qt4reactor.install()
    from twisted.internet import reactor
    Tickle_Control = Tickle_Control(reactor)
    Tickle_Control.show()
    reactor.run()
