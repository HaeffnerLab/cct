from PyQt4 import QtGui
from PyQt4 import QtCore,uic
from twisted.internet.defer import inlineCallbacks, returnValue

updateTime = 100 # ms

class PC (QtGui.QWidget,):
    changedAxis = None
    contAxis = None
    contDirn = None
    stepAxis = None
    stepDirn = None
    frequencyUpdated = False
    freqAxis = None
    voltageUpdated = False
    voltAxis = None
    stepUpdated = False
    posUpdated = False
  
    def __init__(self, reactor, parent=None):
        super(PC, self).__init__(parent)
        self.reactor = reactor
        # self.makeGUI
        self.connect()

    # def makeGUI(self):
        ctrlLayout = QtGui.QGridLayout()
        
        self.axes = ['1', '2', '3']
        self.control = {}
        self.indicator = {}
        self.moving = {}
        self.groupBox = {}
        self.groupBoxLayout = {}
        for axis in self.axes:    
            self.groupBox[axis] = QtGui.QGroupBox(self.axisToName(axis))
            self.groupBoxLayout[axis] = QtGui.QGridLayout()
            self.control[axis + 'u'] = QtGui.QPushButton('step up')
            self.control[axis + 'd'] = QtGui.QPushButton('step down')
            self.control[axis + 's'] = QtGui.QSpinBox()
            self.control[axis + 's'].setSingleStep (1)
            self.control[axis + 's'].setRange (1, 500)
            self.control[axis + 's'].setValue(50)
            self.control[axis + 'spumu'] = QtGui.QDoubleSpinBox()
            self.control[axis + 'spumu'].setValue(1)
            self.control[axis + 'spumu'].setSingleStep(.01)
            self.control[axis + 'spumd'] = QtGui.QDoubleSpinBox()
            self.control[axis + 'spumd'].setValue(.72)            
            self.control[axis + 'spumd'].setSingleStep(.01)
            
            self.indicator[axis + 'v'] = QtGui.QDoubleSpinBox()
            self.indicator[axis + 'v'].setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
            self.indicator[axis + 'v'].setSingleStep(1)
            self.indicator[axis + 'v'].setMaximum(70)
            self.indicator[axis + 'v'].setDecimals(0)
            
            self.indicator[axis + 'f'] = QtGui.QDoubleSpinBox()
            self.indicator[axis + 'f'].setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
            self.indicator[axis + 'f'].setSingleStep(1)
            self.indicator[axis + 'f'].setMaximum(8000)
            self.indicator[axis + 'f'].setDecimals(0)

            self.indicator[axis + 'pos'] = QtGui.QDoubleSpinBox()
            self.indicator[axis + 'pos'].setRange(-2000, 5000)           
            self.indicator[axis + 'pos'].setDecimals(0)

            self.groupBoxLayout[axis].addWidget(QtGui.QLabel('Apx. Pos. [um]'), 2, 0)
            self.groupBoxLayout[axis].addWidget(self.indicator[axis + 'pos'], 3, 0)
            self.groupBoxLayout[axis].addWidget(QtGui.QLabel('steps/um up'), 0, 0)
            self.groupBoxLayout[axis].addWidget(self.control[axis + 'spumu'], 1, 0)
            self.groupBoxLayout[axis].addWidget(QtGui.QLabel('steps/um down'), 4, 0)
            self.groupBoxLayout[axis].addWidget(self.control[axis + 'spumd'], 5, 0)
            self.groupBoxLayout[axis].addWidget(self.control[axis + 'u'], 1, 1)
            self.groupBoxLayout[axis].addWidget(QtGui.QLabel('step size [um]: '), 2, 1)
            self.groupBoxLayout[axis].addWidget(self.control[axis + 's'], 3, 1)
            self.groupBoxLayout[axis].addWidget(self.control[axis + 'd'], 5, 1)
            self.groupBoxLayout[axis].addWidget(QtGui.QLabel('Voltage [V]:'), 6, 0)
            self.groupBoxLayout[axis].addWidget(self.indicator[axis + 'v'], 7, 0)
            self.groupBoxLayout[axis].addWidget(QtGui.QLabel('Frequency [Hz]:'), 6, 1)
            self.groupBoxLayout[axis].addWidget(self.indicator[axis + 'f'], 7, 1)
            self.groupBox[axis].setLayout(self.groupBoxLayout[axis])

            self.control[axis + 'u'].clicked.connect(self.stepPressed(axis, 'u'))
            self.control[axis + 'd'].clicked.connect(self.stepPressed(axis, 'd'))
            self.control[axis + 'spumu'].valueChanged.connect(self.spumChanged(axis, 'u'))
            self.control[axis + 'spumd'].valueChanged.connect(self.spumChanged(axis, 'd'))
            self.indicator[axis + 'pos'].valueChanged.connect(self.posChanged(axis))
            self.indicator[axis + 'v'].valueChanged.connect(self.voltageEntered(axis))
            self.indicator[axis + 'f'].valueChanged.connect(self.frequencyEntered(axis))

	    ctrlLayout.addWidget(self.groupBox[axis], 0, int(axis))      
        
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.Update)
        self.timer.start(updateTime)
            
        self.setLayout(ctrlLayout)
            
    @inlineCallbacks
    def connect(self):
        from labrad.wrappers import connectAsync
        from labrad.types import Error
        self.cxn = yield connectAsync()
        self.piezoserver = yield self.cxn.piezo_server
        self.registry = self.cxn.registry
        for axis in self.axes:
	    yield self.piezoserver.stop(int(axis))
        for axis in self.axes:  
            self.get(axis)  

    @inlineCallbacks
    def Update(self):
        if self.stepUpdated:
            self.stepUpdated = False
            self.posUpdated = True
            if self.stepDirn == 'u':
                yield self.piezoserver.step(int(self.stepAxis), int(round(self.control[self.stepAxis + 's'].value() * self.control[self.stepAxis + 'spumu'].value())))
                self.indicator[self.stepAxis + 'pos'].setValue(self.indicator[self.stepAxis + 'pos'].value() + self.control[self.stepAxis + 's'].value())
            if self.stepDirn == 'd':
                yield self.piezoserver.step(int(self.stepAxis), -int(round(self.control[self.stepAxis + 's'].value() * self.control[self.stepAxis + 'spumd'].value())))
                self.indicator[self.stepAxis + 'pos'].setValue(self.indicator[self.stepAxis + 'pos'].value() - self.control[self.stepAxis + 's'].value())

        elif self.posUpdated:
            self.posUpdated = False
            label = self.posAxis + 'pos'
            yield self.registry.set(label, self.indicator[label].value()) 
                
        elif self.voltageUpdated:
            self.voltageUpdated = False
            yield self.piezoserver.svolt(int(self.voltAxis), int(self.indicator[self.voltAxis + 'v'].value()))            

        elif self.frequencyUpdated:
            self.frequencyUpdated = False
            yield self.piezoserver.sfreq(int(self.freqAxis), int(self.indicator[self.freqAxis + 'f'].value()))            
    
    @inlineCallbacks
    def get(self, axis):
        yield self.piezoserver.gfreq(int(axis))
        sf = yield self.piezoserver.rfreq(int(axis))
        self.indicator[axis + 'f'].setValue(sf)
        yield self.piezoserver.gvolt(int(axis))
        sv = yield self.piezoserver.rvolt(int(axis))
        self.indicator[axis + 'v'].setValue(sv)
        r = self.registry
        r.cd('', 'Piezo Control')
        pos = yield r.get(axis + 'pos')
        self.indicator[axis + 'pos'].setValue(pos)
        spumu = yield r.get(axis + 'spumu')
        self.control[axis + 'spumu'].setValue(spumu)
        spumd = yield r.get(axis + 'spumd')
        self.control[axis + 'spumd'].setValue(spumd)

    def voltageEntered(self, axis):
        def ve():
            self.voltageUpdated = True
            self.voltAxis = axis
        return ve

    def frequencyEntered(self, axis):
        def fe():
            self.frequencyUpdated = True
            self.freqAxis = axis
        return fe
    
    def stepPressed(self, axis, dirn):
        def sp():
            self.stepUpdated = True
            self.stepAxis = axis
            self.stepDirn = dirn
        return sp

    def spumChanged(self, axis, dirn):
        @inlineCallbacks
        def sc(c):
            label = axis + 'spum' + dirn
            yield self.registry.set(label, self.control[label].value())
        return sc

    def posChanged(self, axis):
        def pc():
            self.posAxis = axis
            self.posUpdated = True
        return pc
	
    def axisToName(self, axis):
        if axis == '1': return 'up/down'
        if axis == '2': return 'forward'
        if axis == '3': return 'tilt'
        if axis == '4': return 'sweep'
            
class PIEZO_CONTROL(QtGui.QMainWindow):
    def __init__(self, reactor, parent=None):
        super(PIEZO_CONTROL, self).__init__(parent)
        self.reactor = reactor
        widget = QtGui.QWidget()
        gridLayout = QtGui.QGridLayout()    
        gridLayout.addWidget(PC(reactor), 0, 0)
        self.setWindowTitle('Piezo Control')
        widget.setLayout(gridLayout) 
        self.setCentralWidget(widget) 
                
    def closeEvent(self, x):       
        self.reactor.stop() 
        
if __name__ == "__main__":
    a = QtGui.QApplication( [] )
    import qt4reactor
    qt4reactor.install()
    from twisted.internet import reactor
    PIEZO_CONTROL = PIEZO_CONTROL(reactor)
    PIEZO_CONTROL.show()
    reactor.run()
        
