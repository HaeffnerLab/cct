import sys
import os
from PyQt4 import QtGui, QtCore, uic
from numpy import *
from qtui.QCustomLevelSpin import QCustomLevelSpin
from qtui.QCustomSliderSpin import QCustomSliderSpin
from qtui.QCustomSpinBox import QCustomSpinBox
from twisted.internet.defer import inlineCallbacks, returnValue

UpdateTime = 100 # ms
SIGNALID = 270836
SIGNALID2 = 270835
Nelectrodes = 28

class MULTIPOLE_CONTROL(QtGui.QWidget):
    def __init__(self, reactor, parent=None):
        super(MULTIPOLE_CONTROL, self).__init__(parent)
        self.reactor = reactor
        self.connect()
        
        
    @inlineCallbacks    
    def makeGUI(self):
        self.numWells = yield self.dacserver.return_number_wells()    
        self.ctrlLayout = QtGui.QGridLayout()
        self.controlLabels = ['Ex1','Ey1','Ez1','U1','U2','U3','U4','U5', 'Ex2', 'Ey2', 'Ez2', 'V1', 'V2', 'V3', 'V4', 'V5']
     
        self.controls = {}
        self.controls['Ex1'] = QCustomSpinBox('Ex1', (-2.,2.))
        self.controls['Ey1'] = QCustomSpinBox('Ey1', (-2.,2.))
        self.controls['Ez1'] = QCustomSpinBox('Ez1', (-2.,2.))
        self.controls['U1'] = QCustomSpinBox('U1', (-20.,20.))
        self.controls['U2'] = QCustomSpinBox('U2', (0.,20.))
        self.controls['U3'] = QCustomSpinBox('U3', (-10.,10.))
        self.controls['U4'] = QCustomSpinBox('U4', (-10.,10.))
        self.controls['U5'] = QCustomSpinBox('U5', (-10.,10.))
        self.controls['Ex2'] = QCustomSpinBox('Ex2', (-2.,2.))
        self.controls['Ey2'] = QCustomSpinBox('Ey2', (-2.,2.))
        self.controls['Ez2'] = QCustomSpinBox('Ez2', (-2.,2.))
        self.controls['V1'] = QCustomSpinBox('V1', (-20.,20.))
        self.controls['V2'] = QCustomSpinBox('V2', (0.,20.))
        self.controls['V3'] = QCustomSpinBox('V3', (-10.,10.))
        self.controls['V4'] = QCustomSpinBox('V4', (-10.,10.))
        self.controls['V5'] = QCustomSpinBox('V5', (-10.,10.))
        
        self.multipoleValues = {}
        for k in self.controlLabels:
            self.multipoleValues[k]=0.0

        if self.numWells == 1:
	    self.ctrlLayout.addWidget(self.controls['Ex1'],0,0)
	    self.ctrlLayout.addWidget(self.controls['Ey1'],1,0)
	    self.ctrlLayout.addWidget(self.controls['Ez1'],2,0)
	    self.ctrlLayout.addWidget(self.controls['U1'],0,1)
	    self.ctrlLayout.addWidget(self.controls['U2'],1,1)
	    self.ctrlLayout.addWidget(self.controls['U3'],2,1)
	    self.ctrlLayout.addWidget(self.controls['U4'],3,1)
	    self.ctrlLayout.addWidget(self.controls['U5'],4,1)
        else:
	    self.ctrlLayout.addWidget(self.controls['Ex1'],0,0)
	    self.ctrlLayout.addWidget(self.controls['Ey1'],1,0)
	    self.ctrlLayout.addWidget(self.controls['Ez1'],2,0)
	    self.ctrlLayout.addWidget(self.controls['U1'],0,1)
	    self.ctrlLayout.addWidget(self.controls['U2'],1,1)
	    self.ctrlLayout.addWidget(self.controls['U3'],2,1)
	    self.ctrlLayout.addWidget(self.controls['U4'],3,1)
	    self.ctrlLayout.addWidget(self.controls['U5'],4,1)
	    self.ctrlLayout.addWidget(self.controls['Ex2'],0,2)
	    self.ctrlLayout.addWidget(self.controls['Ey2'],1,2)
	    self.ctrlLayout.addWidget(self.controls['Ez2'],2,2)
	    self.ctrlLayout.addWidget(self.controls['V1'],0,3)
	    self.ctrlLayout.addWidget(self.controls['V2'],1,3)
	    self.ctrlLayout.addWidget(self.controls['V3'],2,3)
	    self.ctrlLayout.addWidget(self.controls['V4'],3,3)
	    self.ctrlLayout.addWidget(self.controls['V5'],4,3)	    	            
        self.multipoleFileSelectButton = QtGui.QPushButton('Set C File')
        self.ctrlLayout.addWidget(self.multipoleFileSelectButton,4,0)

        self.inputUpdated = False
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.sendToServer)
        self.timer.start(UpdateTime)       
        for k in self.controlLabels:
            self.controls[k].onNewValues.connect(self.inputHasUpdated)
        self.multipoleFileSelectButton.released.connect(self.selectCFile)
        self.setLayout(self.ctrlLayout)
        yield self.followSignal(0, 0)
        
    @inlineCallbacks
    def updateGUI(self):
        self.numWells = yield self.dacserver.return_number_wells()
        print "num. wells: " + str(self.numWells)           
	if self.numWells == 2:
	    try:
		self.ctrlLayout.addWidget(self.controls['Ex2'],0,2)
		self.ctrlLayout.addWidget(self.controls['Ey2'],1,2)
		self.ctrlLayout.addWidget(self.controls['Ez2'],2,2)
		self.ctrlLayout.addWidget(self.controls['V1'],0,3)
		self.ctrlLayout.addWidget(self.controls['V2'],1,3)
		self.ctrlLayout.addWidget(self.controls['V3'],2,3)
		self.ctrlLayout.addWidget(self.controls['V4'],3,3)
		self.ctrlLayout.addWidget(self.controls['V5'],4,3)
		print 'k' 
	    except: print "previous Cfile also had 2 wells"
	else:
	    try:
		self.ctrlLayout.removeWidget(self.controls['Ex2'])
		self.ctrlLayout.removeWidget(self.controls['Ey2'])
		self.ctrlLayout.removeWidget(self.controls['Ez2'])
		self.ctrlLayout.removeWidget(self.controls['V1'])
		self.ctrlLayout.removeWidget(self.controls['V2'])
		self.ctrlLayout.removeWidget(self.controls['V3'])
		self.ctrlLayout.removeWidget(self.controls['V4'])
		self.ctrlLayout.removeWidget(self.controls['V5'])
		print 'n'
	    except: print "previous Cfile also had one well"
	yield self.followSignal(0, 0)
	
        
    @inlineCallbacks
    def connect(self):
        from labrad.wrappers import connectAsync
        from labrad.types import Error
        self.cxn = yield connectAsync()
        self.dacserver = yield self.cxn.cctdac_pulser
        yield self.setupListeners()
        yield self.makeGUI()
        
    def inputHasUpdated(self):
        self.inputUpdated = True
        for k in self.controlLabels:
            self.multipoleValues[k] = round(self.controls[k].spinLevel.value(), 3)
        
    def sendToServer(self):
        if self.inputUpdated:
            self.dacserver.set_multipole_values(self.multipoleValues.items())
            self.inputUpdated = False
    
    @inlineCallbacks        
    def selectCFile(self):
        fn = QtGui.QFileDialog().getOpenFileName()
        yield self.dacserver.set_multipole_control_file(1, str(fn))
        self.updateGUI()
        self.inputHasUpdated()
        
    @inlineCallbacks    
    def setupListeners(self):
        yield self.dacserver.signal__ports_updated(SIGNALID)
        yield self.dacserver.addListener(listener = self.followSignal, source = None, ID = SIGNALID) 
        
    @inlineCallbacks
    def followSignal(self, x, s):
	try:
	    multipoles = yield self.dacserver.get_multipole_voltages()
	    for (k,v) in multipoles:
		self.controls[k].setValueNoSignal(v)
	except: print '...'
    
    def closeEvent(self, x):
        self.reactor.stop()  

class CHANNEL_CONTROL (QtGui.QWidget):
    def __init__(self, reactor, parent=None):
        super(CHANNEL_CONTROL, self).__init__(parent)
        self.reactor = reactor
        self.makeGUI()
        self.connect()
     
    def makeGUI(self):
        layout = QtGui.QGridLayout()                                                                            
        self.controlLabels = []
        for i in range(1, Nelectrodes):
	    self.controlLabels.append(str(i))
	    
        self.controls = {}
        for label in self.controlLabels:
	    if int(label) < 6: 
		self.controls[label] = QCustomSpinBox(label, (-30, 30))
	    elif int(label) < 15: 
		self.controls[label] = QCustomSpinBox(str(int(label) - 5) + '   ' , (-30, 30))
	    else:
		self.controls[label] = QCustomSpinBox(str(int(label) - 5) , (-30, 30))
        self.controlLabels.append('CNT')
        self.controls['CNT'] = QCustomSpinBox('CNT', (-30, 30))
        
        self.labelToNumber = {}
        for l in self.controlLabels:
            if l == 'CNT':
                self.labelToNumber[l] = Nelectrodes
            else:
                self.labelToNumber[l] = int(l)

        self.channelValues = {}
        for k in self.controlLabels:
            self.channelValues[k]=0.0
            
	smaBox = QtGui.QGroupBox('SMA Out')
	smaLayout = QtGui.QGridLayout()
	smaBox.setLayout(smaLayout)
	
	elecBox = QtGui.QGroupBox('Electrodes')
	elecLayout = QtGui.QGridLayout()
	elecBox.setLayout(elecLayout)
	layout.addWidget(smaBox, 0, 0)
	layout.addWidget(elecBox, 0, 1)
	
        for j in range(5):
            smaLayout.addWidget(self.controls[str(j+1)],j,1)
        for j in range(5, 16):
	    elecLayout.addWidget(self.controls[str(j+1)],16 - j,1)
	for j in range(16, 27):
	    elecLayout.addWidget(self.controls[str(j+1)],27 - j,5)
        elecLayout.addWidget(self.controls['CNT'], 12, 3)        
        
        layout.setColumnStretch(1, 1)
       
        self.inputUpdated = False                
        self.timer = QtCore.QTimer(self)        
        self.timer.timeout.connect(self.sendToServer)
        self.timer.start(UpdateTime)
        
        for k in self.controlLabels:
            self.controls[k].onNewValues.connect(self.inputHasUpdated(k))
                   
        self.setLayout(layout)
	
            
    @inlineCallbacks
    def connect(self):
        from labrad.wrappers import connectAsync
        from labrad.types import Error
        self.cxn = yield connectAsync()
        self.dacserver = yield self.cxn.cctdac_pulser
        yield self.setupListeners()
        yield self.followSignal(0, 0)

    def inputHasUpdated(self, name):
        def iu():
            self.inputUpdated = True
            for k in self.controlLabels:
                self.channelValues[k] = round(self.controls[k].spinLevel.value(), 3)
            self.changedChannel = name
        return iu

    def sendToServer(self):
        if self.inputUpdated:
            c = self.changedChannel
            self.dacserver.set_individual_analog_voltages([(self.labelToNumber[c], self.channelValues[c])])
            self.inputUpdated = False
            
    @inlineCallbacks    
    def setupListeners(self):
        yield self.dacserver.signal__ports_updated(SIGNALID2)
        yield self.dacserver.addListener(listener = self.followSignal, source = None, ID = SIGNALID2)
    
    @inlineCallbacks
    def followSignal(self, x, s):
        av = yield self.dacserver.get_analog_voltages()
        for (c, v) in zip(self.controlLabels, av):
            self.controls[c].setValueNoSignal(v)

    def closeEvent(self, x):
        self.reactor.stop()        

class CHANNEL_MONITOR(QtGui.QWidget):
    def __init__(self, reactor, parent=None):
        super(CHANNEL_MONITOR, self).__init__(parent)
        self.reactor = reactor
        self.makeGUI()
        self.connect()
        
    def makeGUI(self):      
        self.Nelectrodes = Nelectrodes
        self.electrodes = [QtGui.QLCDNumber() for i in range(self.Nelectrodes)]
        for i in range(self.Nelectrodes):
	    self.electrodes[i].setNumDigits(6)
        
        layout = QtGui.QGridLayout()
        """
        adding ion slider
        """
        
        self.slider = QtGui.QSlider(QtCore.Qt.Vertical)
        self.slider.setTickPosition(2)
        self.slider.setRange(0, 249)
       
        
	smaBox = QtGui.QGroupBox('SMA Out')
	smaLayout = QtGui.QGridLayout()
	smaBox.setLayout(smaLayout)
	
	elecBox = QtGui.QGroupBox('Electrode Voltages')
	elecLayout = QtGui.QGridLayout()
	elecBox.setLayout(elecLayout)
	layout.addWidget(smaBox, 0, 0)
	layout.addWidget(elecBox, 0, 1)
	
        for j in range(5):
            smaLayout.addWidget(QtGui.QLabel(str(j+1)),j,0)
            smaLayout.addWidget(self.electrodes[j],j,1)
        for j in range(5, 16):
	    elecLayout.addWidget(QtGui.QLabel(str(j-4)),16 - j,0)
	    elecLayout.addWidget(self.electrodes[j],16 - j,1)
	    elecLayout.setColumnStretch(1, 1)
	for j in range(16, 27):
	    elecLayout.addWidget(QtGui.QLabel(str(j-4)),27 - j,4)
	    elecLayout.addWidget(self.electrodes[j],27 - j,5)
	    elecLayout.setColumnStretch(5, 1)
	
        elecLayout.addWidget(QtGui.QLabel('CNT'), 12, 2)
        elecLayout.addWidget(self.electrodes[Nelectrodes-1], 12, 3)
        elecLayout.addWidget(self.slider, 2, 3, 9, 1)
        elecLayout.setColumnStretch(3, 1)
        
        self.slider.sliderReleased.connect(self.shuttle)

        self.setLayout(layout)  
                
    @inlineCallbacks
    def connect(self):
        from labrad.wrappers import connectAsync
        from labrad.types import Error
        self.cxn = yield connectAsync()
        self.dacserver = yield self.cxn.cctdac_pulser
        yield self.setupListeners()
        yield self.followSignal(0, 0)        
        
    @inlineCallbacks    
    def setupListeners(self):
        yield self.dacserver.signal__ports_updated(SIGNALID2)
        yield self.dacserver.addListener(listener = self.followSignal, source = None, ID = SIGNALID2)
    
    @inlineCallbacks
    def followSignal(self, x, s):
        av = yield self.dacserver.get_analog_voltages()
        for (e, v) in zip(self.electrodes, av):
            e.display(float(v))
        for (i, v) in zip(range(self.Nelectrodes), av):
            if math.fabs(v) > 40:
                self.electrodes[i].setStyleSheet("QWidget {background-color: orange }")
                self.electrodes[i].setAutoFillBackground(True)
            if math.fabs(v) < 40:
                self.electrodes[i].setStyleSheet("QWidget {background-color:  }")
                self.electrodes[i].setAutoFillBackground(False)     
                
    @inlineCallbacks
    def shuttle(self):
        #yield self.dacserver.do_nothing()
        yield self.dacserver.shuttle_ion(self.slider.value() + 1)
        print self.slider.value()
        yield self.followSignal(0, 0)
       
    def closeEvent(self, x):
        self.reactor.stop()

class DAC_CONTROL(QtGui.QMainWindow):
    def __init__(self, reactor, parent=None):
        super(DAC_CONTROL, self).__init__(parent)
        self.reactor = reactor

        channelControlTab = self.buildChannelControlTab()        
        multipoleControlTab = self.buildMultipoleControlTab()
        scanTab = self.buildScanTab()
        tab = QtGui.QTabWidget()
        tab.addTab(multipoleControlTab,'&Multipoles')
        tab.addTab(channelControlTab, '&Channels')
        tab.addTab(scanTab, '&Scans')
        self.setCentralWidget(tab)
    
    def buildMultipoleControlTab(self):
        widget = QtGui.QWidget()
        gridLayout = QtGui.QGridLayout()
        gridLayout.addWidget(CHANNEL_MONITOR(self.reactor),0,0)
        gridLayout.addWidget(MULTIPOLE_CONTROL(self.reactor),0,1)
        widget.setLayout(gridLayout)
        return widget

    def buildChannelControlTab(self):
        widget = QtGui.QWidget()
        gridLayout = QtGui.QGridLayout()
        gridLayout.addWidget(CHANNEL_CONTROL(self.reactor),0,0)
        widget.setLayout(gridLayout)
        return widget
        
    def buildScanTab(self):
	from SCAN_Ex_and_TICKLE import Scan_Control_Ex_and_Tickle
	from SCAN_Ey_and_TICKLE import Scan_Control_Ey_and_Tickle
	widget = QtGui.QWidget()
	gridLayout = QtGui.QGridLayout()
	#gridLayout.addWidget(Scan_Control_Ex_and_Tickle(self.reactor), 0, 0)
	#gridLayout.addWidget(Scan_Control_Ey_and_Tickle(self.reactor), 0, 1)
	widget.setLayout(gridLayout)
	return widget
    
    def closeEvent(self, x):
        self.reactor.stop()  

if __name__ == "__main__":
    a = QtGui.QApplication( [] )
    import qt4reactor
    qt4reactor.install()
    from twisted.internet import reactor
    DAC_CONTROL = DAC_CONTROL(reactor)
    DAC_CONTROL.show()
    reactor.run()
