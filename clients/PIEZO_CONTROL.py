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
    checkNext = None
    frequencyUpdated = False
    freqAxis = None
    voltageUpdated = False
    voltAxis = None
    stepUpdated = False
    continuousUpdated = False
  
    def __init__(self, reactor, parent=None):
        super(PC, self).__init__(parent)
        self.reactor = reactor
        self.connect()

        ctrlLayout = QtGui.QGridLayout()
        
        self.axes = ['1', '2', '3']
        self.control = {}
        self.indicator = {}
        self.moving = {}
        self.step = {}
        self.groupBox = {}
        self.groupBoxLayout = {}
        for axis in self.axes:
    
            self.groupBox[axis] = QtGui.QGroupBox(self.axisToName(axis))
            self.groupBoxLayout[axis] = QtGui.QGridLayout()
            self.control[axis + 'u'] = QtGui.QPushButton('step up')
            self.control[axis + 'd'] = QtGui.QPushButton('step down')
            self.control[axis + 'U'] = QtGui.QPushButton('continuous up')
            self.control[axis + 'D'] = QtGui.QPushButton('continuous down')
            self.control[axis + 'U'].setCheckable(True)
            self.control[axis + 'D'].setCheckable(True)
            self.control[axis + 's'] = QtGui.QSpinBox()
            self.control[axis + 's'].setSingleStep (1)
            self.control[axis + 's'].setRange (1, 500)
            self.control[axis + 's'].setValue(50)
            self.control[axis + 's'].setPrefix('steps: ')
            
            self.indicator[axis + 'v'] = QtGui.QDoubleSpinBox()
            self.indicator[axis + 'v'].setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
            self.indicator[axis + 'v'].setPrefix('Voltage: ')
            self.indicator[axis + 'v'].setSingleStep(1)
            self.indicator[axis + 'v'].setSuffix(' V')
            self.indicator[axis + 'v'].setMaximum(70)
            self.indicator[axis + 'v'].setMinimum(0)
            self.indicator[axis + 'v'].setDecimals(0)
            
            self.indicator[axis + 'f'] = QtGui.QDoubleSpinBox()
            self.indicator[axis + 'f'].setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
            self.indicator[axis + 'f'].setPrefix('Frequency: ')
            self.indicator[axis + 'f'].setSuffix(' Hz')
            self.indicator[axis + 'f'].setSingleStep(1)
            self.indicator[axis + 'f'].setMaximum(8000)
            self.indicator[axis + 'f'].setDecimals(0)
	    
	    self.step[axis + 'u'] = False
	    self.step[axis + 'd'] = False
            self.moving[axis + 'U'] = False
            self.moving[axis + 'D'] = False
            
            self.groupBoxLayout[axis].addWidget(self.control[axis + 'U'],0,1)
            self.groupBoxLayout[axis].addWidget(self.control[axis + 'u'],0,0)
            self.groupBoxLayout[axis].addWidget(self.control[axis + 's'],1,0)
            self.groupBoxLayout[axis].addWidget(self.control[axis + 'd'],2,0)
            self.groupBoxLayout[axis].addWidget(self.control[axis + 'D'],2,1)
            self.groupBoxLayout[axis].addWidget(self.indicator[axis + 'v'], 3,0)
            self.groupBoxLayout[axis].addWidget(self.indicator[axis + 'f'], 3,1)
            self.groupBox[axis].setLayout(self.groupBoxLayout[axis])

            self.control[axis + 'U'].clicked.connect(self.continuousPressed(axis, 'U'))
            self.control[axis + 'u'].clicked.connect(self.stepPressed(axis, 'u'))
            self.control[axis + 'd'].clicked.connect(self.stepPressed(axis, 'd'))
            self.control[axis + 'D'].clicked.connect(self.continuousPressed(axis, 'D'))
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
        self.piezoserver = yield self.cxn.cctmain_piezo_server
        for axis in self.axes:
	    yield self.piezoserver.stop(int(axis))
	for axis in self.axes:  
            self.get(axis)  

    @inlineCallbacks
    def Update(self):
	if self.stepUpdated:
	    if self.stepDirn == 'u':
		yield self.piezoserver.step(int(self.stepAxis), self.control[self.stepAxis + 's'].value())
	    if self.stepDirn == 'd':
		yield self.piezoserver.step(int(self.stepAxis), -self.control[self.stepAxis + 's'].value())	
	    self.checkNext = True	
	    self.checkAxis = self.stepAxis
	elif self.continuousUpdated:
	    if self.moving[self.contAxis + self.contDirn]:
		yield self.piezoserver.continuous(int(self.contAxis), self.contDirn)
	    else:
		yield self.piezoserver.stop(int(self.contAxis))
		self.get(self.contAxis)
	elif self.voltageUpdated:
	    yield self.piezoserver.svolt(int(self.voltAxis), int(self.indicator[self.voltAxis + 'v'].value()))
	    self.voltageUpdated = False
	    self.checkNext = True
	    self.checkAxis = self.voltAxis
	elif self.frequencyUpdated:
	    yield self.piezoserver.sfreq(int(self.freqAxis), int(self.indicator[self.freqAxis + 'f'].value()))
	    self.frequencyUpdated = False
	    self.checkNext = True
	    self.checkAxis = self.freqAxis
	if self.checkNext:
	    self.checkNext = False
	    self.get(self.checkAxis)
	self.stepUpdated = False
	self.continuousUpdated = False 
    
    @inlineCallbacks
    def get(self, axis):
	yield self.piezoserver.gfreq(int(axis))
	sf = yield self.piezoserver.rfreq(int(axis))
	self.indicator[axis + 'f'].setValue(sf)
	yield self.piezoserver.gvolt(int(axis))
	sv = yield self.piezoserver.rvolt(int(axis))
	self.indicator[axis + 'v'].setValue(sv)

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
	
    def continuousPressed(self, axis, dirn):
        def cp():
            self.continuousUpdated = True
            self.moving[axis + dirn]  = not self.moving[axis + dirn]
            self.contAxis = axis
            self.contDirn = dirn
        return cp
    
    def stepPressed(self, axis, dirn):
	def sp():
	    self.stepUpdated = True
	    self.stepAxis = axis
	    self.stepDirn = dirn
	return sp
	
    def axisToName(self, axis):
	if axis == '1':
	    return 'up/down'
	if axis == '2':
	    return 'forward'
	if axis == '3':
	    return 'tilt'
	if axis == '4':
	    return 'sweep'
    
    def op(self, dirn):
	if dirn == 'U':
	    return 'D'
	if dirn == 'D':
	    return 'U'
            
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
        
