import sys;
sys.path.append('/home/cct/LabRAD/cct/scripts/simpleMeasurements/FFT')
import os
from PyQt4 import QtGui
from PyQt4 import QtCore,uic
import numpy
import datetime
import time as TIME
from twisted.internet.defer import inlineCallbacks, returnValue

DminAmp = .1
DmaxAmp = .2
DsizeStepsAmp = .01
DnumStepsAmp = (DmaxAmp - DminAmp)/DsizeStepsAmp
Davg = 6
DminTfrq = 45.4
DmaxTfrq = 45.8
DsizeStepsTfrq = .015
DnumStepsTfrq = (DmaxTfrq - DminTfrq)/DsizeStepsTfrq

class Ex(QtGui.QWidget):
    def __init__(self, reactor, parent=None):
	super(Ex,self).__init__(parent)
	self.running = False
	self.reactor = reactor
	self.makeGUI()
	self.connect()
	
    #@inlineCallbacks
    def makeGUI(self):
	layout = QtGui.QGridLayout()
	groupBox = QtGui.QGroupBox('Scan Ex and Tickle')
	groupBoxLayout = QtGui.QGridLayout()
	self.controlLabels = ['minAmp', 'maxAmp', 'numStepsAmp', 'sizeStepsAmp', 'avg', 'minTfrq', 'maxTfrq', 'numStepsTfrq', 'sizeStepsTfrq' ]
	self.control = {}
	for label in self.controlLabels:
	    self.control[label] = QtGui.QDoubleSpinBox()
	    self.control[label].setDecimals(4)
	self.label = {}
	self.control['minAmp'].setValue(DminAmp)
	self.control['minAmp'].setRange(-10,10)
	self.label['minAmp'] = QtGui.QLabel('minimum Ex [V/m]:')
	self.control['maxAmp'].setValue(DmaxAmp)
	self.control['maxAmp'].setRange(-10, 10)
	self.label['maxAmp'] = QtGui.QLabel('maximum Ex [V/m]:')
	self.control['numStepsAmp'].setValue(DnumStepsAmp)
	self.label['numStepsAmp'] = QtGui.QLabel('number of Ex steps:')
	self.control['sizeStepsAmp'].setValue(DsizeStepsAmp)
	self.label['sizeStepsAmp'] = QtGui.QLabel('Ex step size [V/m]:')
	self.control['avg'].setValue(Davg)
	self.control['avg'].setDecimals(0)
	self.label['avg'] = QtGui.QLabel('number to average:')
	self.control['minTfrq'].setValue(DminTfrq)
	self.label['minTfrq'] = QtGui.QLabel('minimum tickle frq [MHz]:')
	self.control['maxTfrq'].setValue(DmaxTfrq)
	self.label['maxTfrq'] = QtGui.QLabel('maximum tickle frq [MHz]:')
	self.control['numStepsTfrq'].setValue(DnumStepsTfrq)
	self.label['numStepsTfrq'] = QtGui.QLabel('number of tickle steps:')
	self.control['sizeStepsTfrq'].setValue(DsizeStepsTfrq)
	self.label['sizeStepsTfrq'] = QtGui.QLabel('tickle step size:')
	self.control['scan'] = QtGui.QPushButton('Scan')
	self.control['stop'] = QtGui.QPushButton('Stop')
	self.control['revAmp'] = QtGui.QCheckBox('reverse')
	self.control['revT'] = QtGui.QCheckBox('reverse')
	groupBox.setLayout(groupBoxLayout)
	layout.addWidget(groupBox, 0, 0)
	for i, l in enumerate(self.controlLabels):
	    groupBoxLayout.addWidget(self.control[l], i, 1)
	    groupBoxLayout.addWidget(self.label[l], i, 0)
	groupBoxLayout.addWidget(self.control['scan'], len(self.controlLabels) + 1, 0, 1, 2)
	groupBoxLayout.addWidget(self.control['stop'], len(self.controlLabels) + 2, 0, 1, 2)
	groupBoxLayout.addWidget(self.control['revAmp'], 3, 2)
	groupBoxLayout.addWidget(self.control['revT'], 8, 2)
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
        self.control['numStepsTfrq'].valueChanged.connect(self.numTStepsChanged)
        self.control['sizeStepsTfrq'].valueChanged.connect(self.sizeTStepsChanged)
        self.control['scan'].clicked.connect(self.scan)
        self.control['stop'].clicked.connect(self.stopScan)
        
    def numAStepsChanged(self):
	if self.control['numStepsAmp'].value() == 0:
	    return
	newSize = round((self.control['maxAmp'].value() - self.control['minAmp'].value())/self.control['numStepsAmp'].value(), 4)
	self.control['sizeStepsAmp'].setValue(newSize)
	
    def sizeAStepsChanged(self):
	if self.control['sizeStepsAmp'].value() == 0:
	    return
	newNum = round((self.control['maxAmp'].value() - self.control['minAmp'].value())/self.control['sizeStepsAmp'].value(), 4)
	self.control['numStepsAmp'].setValue(newNum)
	
    def numTStepsChanged(self):
	if self.control['numStepsTfrq'].value() == 0:
	    return      
	newSize = round((self.control['maxTfrq'].value() - self.control['minTfrq'].value())/self.control['numStepsTfrq'].value(), 4)
	self.control['sizeStepsTfrq'].setValue(newSize)	
	
    def sizeTStepsChanged(self):
	if self.control['sizeStepsTfrq'].value() == 0:
	    return      
	newNum = round((self.control['maxTfrq'].value() - self.control['minTfrq'].value())/self.control['sizeStepsTfrq'].value(), 4)
	self.control['numStepsTfrq'].setValue(newNum)
	
    @inlineCallbacks  
    def scan(self, c):
	self.control['scan'].setText('Scan is running')
	self.running = True
	yield self.rs.onoff(True)
	now = datetime.datetime.now()
	date = now.strftime("%Y%m%d")
	time = now.strftime('%H%M%S')

	amplitudes = numpy.arange(self.control['minAmp'].value(), self.control['maxAmp'].value(), self.control['sizeStepsAmp'].value())
	if self.control['revAmp'].isChecked():
	    amplitudes = amplitudes[::-1]
	frequencies = numpy.arange(self.control['minTfrq'].value(), self.control['maxTfrq'].value(), self.control['sizeStepsTfrq'].value())
	print frequencies
	if self.control['revT'].isChecked():	    
	    frequencies = frequencies[::-1] # The ion asks that you kindly scan downwards, thanks
	print self.control['revT'].isChecked()
	listy = yield self.ds.get_multipole_voltages()
	for i in range(8):
	    if listy[i][0] == 'Ey':
		Ey = listy[i][1]
	    if listy[i][0] == 'Ex':
		Exi = listy[i][1]
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
	    yield self.dv.cd(['', date, 'QuickMeasurements','MMComp', time + '-Ex and Tickle'],True)
	    name = yield self.dv.new('Ex: ' + str(Ex),[('Frequency', 'Hz')], [('PMT Counts', 'PMT counts', 'PMT counts')])
	    yield self.dv.add_parameter('Ex', Ex)
	    yield self.dv.add_parameter('plotLive',True)
	    print 'Saving {}'.format(name)
	    yield self.ds.set_multipole_voltages([('Ex', Ex), ('Ey', Ey), ('Ez', Ez), ('U1', U1), ('U2', U2), ('U3', U3), ('U4', U4), ('U5', U5)])
	    for f in frequencies:
		if self.running == False:
		    yield self.rs.onoff(False)
		    yield self.ds.set_multipole_voltages([('Ex', Exi), ('Ey', Ey), ('Ez', Ez), ('U1', U1), ('U2', U2), ('U3', U3), ('U4', U4), ('U5', U5)])
		    self.control['scan'].setText('Scan')
		    return
		self.rs.frequency(f)
		TIME.sleep(.3)
		pmtcount = yield self.pmt.get_next_counts('ON', int(self.control['avg'].value()), True)				
		yield self.dv.add(f, pmtcount)
	yield self.rs.onoff(False)
	yield self.ds.set_multipole_voltages([('Ex', Exi), ('Ey', Ey), ('Ez', Ez), ('U1', U1), ('U2', U2), ('U3', U3), ('U4', U4), ('U5', U5)])
	self.control['scan'].setText('Scan')
	    
    def stopScan(self, c):
	self.running = False
	
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
        self.setWindowTitle('Scan Ex and Tickle Control')
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