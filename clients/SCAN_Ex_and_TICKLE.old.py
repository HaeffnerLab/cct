import sys;
sys.path.append('/home/cct/LabRAD/cct/scripts/simpleMeasurements/FFT')
import os
from PyQt4 import QtGui
from PyQt4 import QtCore,uic
import numpy
import datetime
from twisted.internet.defer import inlineCallbacks, returnValue

DminAmp = .1
DmaxAmp = .2
DsizeStepsAmp = .01
DnumStepsAmp = (DmaxAmp - DminAmp)/DsizeStepsAmp
DrecTime = .5
Davg = 6
DfrqSpan = 100
DfrqOff = -920
DminTfrq = 45.4
DmaxTfrq = 45.8
DsizeStepsTfrq = .015
DnumStepsTfrq = (DmaxTfrq - DminTfrq)/DsizeStepsTfrq

class Ex(QtGui.QWidget):
    def __init__(self, reactor, parent=None):
	super(Ex,self).__init__(parent)
	self.reactor = reactor
	self.makeGUI()
	self.connect()
	
    #@inlineCallbacks
    def makeGUI(self):
	layout = QtGui.QGridLayout()
	groupBox = QtGui.QGroupBox('Scan Ex and Tickle')
	groupBoxLayout = QtGui.QGridLayout()
	self.controlLabels = ['minAmp', 'maxAmp', 'numStepsAmp', 'sizeStepsAmp', 'recTime', 'avg', 'frqSpan', 'frqOff', 'minTfrq', 'maxTfrq', 'numStepsTfrq', 'sizeStepsTfrq' ]
	self.control = {}
	for label in self.controlLabels:
	    self.control[label] = QtGui.QDoubleSpinBox()
	self.control['minAmp'].setValue(DminAmp)
	self.control['minAmp'].setPrefix('min. Ex: ')
	self.control['minAmp'].setSuffix(' V/m')
	self.control['maxAmp'].setValue(DmaxAmp)
	self.control['maxAmp'].setPrefix('max. Ex: ')
	self.control['maxAmp'].setSuffix(' V/m')
	self.control['numStepsAmp'].setValue(DnumStepsAmp)
	self.control['numStepsAmp'].setPrefix('num. steps: ')
	self.control['sizeStepsAmp'].setValue(DsizeStepsAmp)
	self.control['sizeStepsAmp'].setPrefix('step size: ')
	self.control['sizeStepsAmp'].setDecimals(4)
	self.control['recTime'].setValue(DrecTime)
	self.control['recTime'].setPrefix('rec. time: ')
	self.control['recTime'].setSuffix(' s')
	self.control['avg'].setValue(Davg)
	self.control['avg'].setPrefix('average: ')
	self.control['avg'].setDecimals(0)
	self.control['frqSpan'].setValue(DfrqSpan)
	self.control['frqSpan'].setPrefix('f. span: ')
	self.control['frqSpan'].setSuffix(' Hz')
	self.control['frqSpan'].setRange(-999, 999)
	self.control['frqSpan'].setDecimals(0)
	self.control['frqOff'].setValue(DfrqOff)
	self.control['frqOff'].setPrefix('f. offset: ')
	self.control['frqOff'].setSuffix(' Hz')
	self.control['frqOff'].setRange(-9999, 9999)
	self.control['frqOff'].setDecimals(0)
	self.control['minTfrq'].setValue(DminTfrq)
	self.control['minTfrq'].setPrefix('min. Tfrq: ')
	self.control['minTfrq'].setSuffix(' MHz')
	self.control['maxTfrq'].setValue(DmaxTfrq)
	self.control['maxTfrq'].setPrefix('max. Tfrq: ')
	self.control['maxTfrq'].setSuffix(' MHz')
	self.control['numStepsTfrq'].setValue(DnumStepsTfrq)
	self.control['numStepsTfrq'].setPrefix('num. steps: ')
	self.control['sizeStepsTfrq'].setValue(DsizeStepsTfrq)
	self.control['sizeStepsTfrq'].setPrefix('step size: ')	
	self.control['scan'] = QtGui.QPushButton('Scan')
	groupBox.setLayout(groupBoxLayout)
	layout.addWidget(groupBox, 0, 0)
	groupBoxLayout.addWidget(self.control['minAmp'], 0, 0)
	groupBoxLayout.addWidget(self.control['maxAmp'], 1, 0)
	groupBoxLayout.addWidget(self.control['numStepsAmp'], 2, 0)
	groupBoxLayout.addWidget(self.control['sizeStepsAmp'], 3, 0)
	groupBoxLayout.addWidget(self.control['minTfrq'], 0, 1)
	groupBoxLayout.addWidget(self.control['maxTfrq'], 1, 1)
	groupBoxLayout.addWidget(self.control['numStepsTfrq'], 2, 1)
	groupBoxLayout.addWidget(self.control[	'sizeStepsTfrq'], 3, 1)
	groupBoxLayout.addWidget(self.control['recTime'],0, 2)
	groupBoxLayout.addWidget(self.control['avg'], 1, 2) 
	groupBoxLayout.addWidget(self.control['frqSpan'], 2, 2)
	groupBoxLayout.addWidget(self.control['frqOff'], 3, 2)
	groupBoxLayout.addWidget(self.control['scan'], 4, 0, 1, 3)
	self.setLayout(layout)
	
    @inlineCallbacks
    def connect(self):
        from labrad.wrappers import connectAsync
        from labrad.types import Error
        self.cxn = yield connectAsync()
        self.cxncam = yield connectAsync('192.168.169.30')
        self.dv = yield self.cxn.data_vault
        self.ds = yield self.cxn.cctdac
        self.pmt = self.cxn.normalpmtflow
        self.rs = self.cxncam.rohdeschwarz_server
        self.rs.select_device('GPIB Bus - USB0::0x0AAD::0x0054::104543')
        self.control['numStepsAmp'].valueChanged.connect(self.numAStepsChanged)
        self.control['sizeStepsAmp'].valueChanged.connect(self.sizeAStepsChanged)
        self.control['numStepsAmp'].valueChanged.connect(self.numTStepsChanged)
        self.control['sizeStepsAmp'].valueChanged.connect(self.sizeTStepsChanged)
        self.control['scan'].clicked.connect(self.scan)
        
    def numAStepsChanged(self):
	newSize = (self.control['maxAmp'].value() - self.control['minAmp'].value())/self.control['numStepsAmp'].value()
	self.control['sizeStepsAmp'].setValue(newSize)
	
    def sizeAStepsChanged(self):
	newNum = (self.control['maxAmp'].value() - self.control['minAmp'].value())/self.control['sizeStepsAmp'].value()
	self.control['numStepsAmp'].setValue(newNum)
	
    def numTStepsChanged(self):
	newSize = (self.control['maxTfrq'].value() - self.control['minTfrq'].value())/self.control['numStepsTfrq'].value()
	self.control['sizeStepsTfrq'].setValue(newSize)	
	
    def sizeTStepsChanged(self):
	newNum = (self.control['maxTfrq'].value() - self.control['minTfrq'].value())/self.control['sizeStepsTfrq'].value()
	self.control['numStepsTfrq'].setValue(newNum)
	
    @inlineCallbacks  
    def scan(self, c):
	now = datetime.datetime.now()
	date = now.strftime("%Y%m%d")
	time = now.strftime('%H%M%S')

	amplitudes = numpy.arange(self.control['minAmp'].value(), self.control['maxAmp'].value(), self.control['sizeStepsAmp'].value())
	frequencies = numpy.arange(self.control['minTfrq'].value(), self.control['maxTfrq'].value(), self.control['sizeStepsTfrq'].value())
	frequencies = frequencies[::-1] # The ion asks that you kindly scan downwards, thanks
	listy = yield self.ds.get_multipole_voltages()
	for i in range(8):
	    if listy[i][0] == 'Ey':
		Ey = listy[i][1]
	    if listy[i][0] == 'Ez':
		Ez = listy[i][1]
	    if listy[i][0] == 'U1':
		U1 = listy[i][1]
	    if listy[i][0] == 'U2':
		U2 = listy[i][1]
	    if listy[i][0] == 'U3':
		U3 = listy[i][1]
	    if listy[i][0] == 'U4':
		U4 = listy[i][1]
	    if listy[i][0] == 'U5':
		U5 = listy[i][1]
	for Ex in amplitudes:
	    from labrad.wrappers import connectAsync
	    from labrad.types import Error
	    self.cxn = yield connectAsync()
	    self.cxncam = yield connectAsync('192.168.169.30')
	    self.dv = yield self.cxn.data_vault
	    self.ds = yield self.cxn.cctdac
	    self.pmt = self.cxn.normalpmtflow
	    self.rs = self.cxncam.rohdeschwarz_server
	    self.rs.select_device('GPIB Bus - USB0::0x0AAD::0x0054::104543')
	    yield self.dv.cd(['', date, 'QuickMeasurements','MMComp', time + '-Ex and Tickle'],True)
	    name = yield self.dv.new('',[('Frequency', 'Hz')], [('PMT Counts', 'counts', 'counts')])
	    yield self.dv.add_parameter('Ex', Ex)
	    yield self.dv.add_parameter('plotLive',True)
	    print 'Saving {}'.format(name)
	    yield self.ds.set_multipole_voltages([('Ex', Ex), ('Ey', Ey), ('Ez', Ez), ('U1', U1), ('U2', U2), ('U3', U3), ('U4', U4), ('U5', U5)])
	    for f in frequencies:
		self.rs.frequency(f)
		pmtcount = yield self.pmt.get_next_counts('ON', int(self.control['avg'].value()), True)				
		yield self.dv.add(f, pmtcount)
	    
	    
    def closeEvent(self, x):
        self.reactor.stop()
        
class Scan_Control_Ex_and_Tickle(QtGui.QMainWindow):
    def __init__(self, reactor, parent=None):
        super(Scan_Control_Ex_and_Tickle, self).__init__(parent)
        self.reactor = reactor
        W = self.buildW(reactor)
        widget = QtGui.QWidget()
        gridLayout = QtGui.QGridLayout()    
        gridLayout.addWidget(W, 0, 0)
        self.setWindowTitle('Scan Ex Control')
        widget.setLayout(gridLayout) 
        self.setCentralWidget(widget)

    def buildW(self, reactor):
        W = QtGui.QWidget()
        subLayout = QtGui.QGridLayout()
        subLayout.addWidget(Ex(reactor), 0, 0)
        W.setLayout(subLayout)
        return W
                
    def closeEvent(self, x):
        self.reactor.stop()       
        
if __name__=="__main__":
    a = QtGui.QApplication( [] )
    import qt4reactor
    qt4reactor.install()
    from twisted.internet import reactor
    Scan_Control_Ex_and_Tickle = Scan_Control_Ex_and_Tickle(reactor)
    Scan_Control_Ex_and_Tickle.show()
    reactor.run()        