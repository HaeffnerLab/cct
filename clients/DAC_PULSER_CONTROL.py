import sys
import os
from PyQt4 import QtGui
from PyQt4 import QtCore,uic
from numpy import *
from qtui.QDACControl import QDACControl
from qtui.QCustomLevelSpin import QCustomLevelSpin
from qtui.QCustomSliderSpin import QCustomSliderSpin
from twisted.internet.defer import inlineCallbacks, returnValue

UpdateTime = 100 # ms
SIGNALID = 270836
SIGNALID2 = 270835

class MULTIPOLE_CONTROL(QtGui.QWidget):
    def __init__(self, reactor, parent=None):
        super(MULTIPOLE_CONTROL, self).__init__(parent)
        self.reactor = reactor
        self.connect()
        
        ctrlLayout = QtGui.QGridLayout() 
               
        self.controlLabels = ['Ex','Ey','Ez','U1','U2','U3','U4','U5']
        
        self.controls = {}
        self.controls['Ex'] = QCustomLevelSpin('Ex', (-2.,2.))
        self.controls['Ey'] = QCustomLevelSpin('Ey', (-2.,2.))
        self.controls['Ez'] = QCustomLevelSpin('Ez', (-2.,2.))
        self.controls['U1'] = QCustomLevelSpin('U1', (-20.,20.))
        self.controls['U2'] = QCustomLevelSpin('U2', (0.,20.))
        self.controls['U3'] = QCustomLevelSpin('U3', (-10.,10.))
        self.controls['U4'] = QCustomLevelSpin('U4', (-10.,10.))
        self.controls['U5'] = QCustomLevelSpin('U5', (-10.,10.))
        
        self.multipoleValues = {}
        for k in self.controlLabels:
            self.multipoleValues[k]=0.0

        ctrlLayout.addWidget(self.controls['Ex'],0,0)
        ctrlLayout.addWidget(self.controls['Ey'],1,0)
        ctrlLayout.addWidget(self.controls['Ez'],2,0)
        ctrlLayout.addWidget(self.controls['U1'],0,1)
        ctrlLayout.addWidget(self.controls['U2'],1,1)
        ctrlLayout.addWidget(self.controls['U3'],2,1)
        ctrlLayout.addWidget(self.controls['U4'],3,1)
        ctrlLayout.addWidget(self.controls['U5'],4,1)
        
        self.multipoleFileSelectButton = QtGui.QPushButton('Set C File')
        ctrlLayout.addWidget(self.multipoleFileSelectButton,4,0)

        self.inputUpdated = False
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.sendToServer)
        self.timer.start(UpdateTime)
        
        for k in self.controlLabels:
            self.controls[k].onNewValues.connect(self.inputHasUpdated)
            
        self.multipoleFileSelectButton.released.connect(self.selectCFile)
        
        self.setLayout(ctrlLayout)
        
        
        
    @inlineCallbacks
    def connect(self):
        from labrad.wrappers import connectAsync
        from labrad.types import Error
        self.cxn = yield connectAsync()
        self.dacserver = yield self.cxn.cctdac_pulser
        yield self.setupListeners()
        
    def inputHasUpdated(self):
        self.inputUpdated = True
        print "in inputHasUpdated"
        for k in self.controlLabels:
            self.multipoleValues[k] = round(self.controls[k].spinLevel.value(), 3)
        
    def sendToServer(self):
        if self.inputUpdated:
            print "sending to server ", self.multipoleValues
            print 'why?'
            self.dacserver.set_multipole_voltages(self.multipoleValues.items())
            print "set the values"
            self.inputUpdated = False
            
    def selectCFile(self):
        fn = QtGui.QFileDialog().getOpenFileName()
        self.dacserver.set_multipole_control_file(str(fn))
        
    @inlineCallbacks    
    def setupListeners(self):
        yield self.dacserver.signal__ports_updated(SIGNALID)
        yield self.dacserver.addListener(listener = self.followSignal, source = None, ID = SIGNALID) #cxzv 
    
    def followSignal(self, x, (s)):
        """
        Update the sliders
        """
        multipoles = yield self.dacserver.get_multipole_voltages()
        for (k,v) in multipoles:
           self.controls[k].setValueNoSignal(v)
    
    def closeEvent(self, x):
        self.reactor.stop()  

class CHANNEL_CONTROL (QtGui.QWidget):
    def __init__(self, reactor, parent=None):
        super(CHANNEL_CONTROL, self).__init__(parent)
        self.reactor = reactor
        self.connect()
        
        ctrlLayout = QtGui.QGridLayout()
        
        self.controlLabels = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','CNT']
        
        self.labelToNumber = {}
        for k in self.controlLabels:
            if k == 'CNT':
                self.labelToNumber[k]=18
            else:
                self.labelToNumber[k]=int(k)

        self.controls = {}
        for label in self.controlLabels:
            self.controls[label] = QCustomLevelSpin(label, (-10,10))
              
        self.channelValues = {}
        for k in self.controlLabels:
            self.channelValues[k]=0.0
        
        self.oldValues = {}
        for k in self.controlLabels:
            self.oldValues[k]=0.0
       
        ctrlLayout.addWidget(self.controls['1'],0,0)
        ctrlLayout.addWidget(self.controls['2'],1,0)
        ctrlLayout.addWidget(self.controls['3'],2,0)
        ctrlLayout.addWidget(self.controls['4'],3,0)
        ctrlLayout.addWidget(self.controls['5'],4,0)
        ctrlLayout.addWidget(self.controls['6'],5,0)
        ctrlLayout.addWidget(self.controls['7'],0,1)
        ctrlLayout.addWidget(self.controls['8'],1,1)
        ctrlLayout.addWidget(self.controls['9'],2,1)
        ctrlLayout.addWidget(self.controls['10'],3,1)
        ctrlLayout.addWidget(self.controls['11'],4,1)
        ctrlLayout.addWidget(self.controls['12'],5,1)
        ctrlLayout.addWidget(self.controls['13'],0,2)
        ctrlLayout.addWidget(self.controls['14'],1,2)
        ctrlLayout.addWidget(self.controls['15'],2,2)
        ctrlLayout.addWidget(self.controls['16'],3,2)
        ctrlLayout.addWidget(self.controls['17'],4,2)
        ctrlLayout.addWidget(self.controls['CNT'],5,2)
                
        self.inputUpdated = False                
        self.timer = QtCore.QTimer(self)        
        self.timer.timeout.connect(self.sendToServer)
        self.timer.start(UpdateTime)
        
        for k in self.controlLabels:
            self.controls[k].onNewValues.connect(self.inputHasUpdated2(k))
                   
        self.setLayout(ctrlLayout)
        

            
    @inlineCallbacks
    def connect(self):
        from labrad.wrappers import connectAsync
        from labrad.types import Error
        self.cxn = yield connectAsync()
        self.dacserver = yield self.cxn.cctdac_pulser
        yield self.setupListeners()

    def inputHasUpdated2(self,name):
        def iu():
            self.inputUpdated = True
            print "in inputHasUpdated"
            self.oldValues = self.channelValues.copy() 
            for k in self.controlLabels:
                self.channelValues[k] = round(self.controls[k].spinLevel.value(), 3)
            self.changedChannel = name
            print "Channel changed: " + name
        return iu

    def sendToServer(self):
        if self.inputUpdated:
            c = self.changedChannel
            print 'hi'
            self.dacserver.set_individual_analog_voltages([(self.labelToNumber[c], self.channelValues[c])])
            print [(self.labelToNumber[c], self.channelValues[c])]
            print "set the values"
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
    """
    A widget to monitor each of the DAC channel voltages.
    """
    
    def __init__(self, reactor, Nelectrodes, parent=None):
        super(CHANNEL_MONITOR, self).__init__(parent)
        self.reactor = reactor
        self.connect()
        
        self.Nelectrodes = Nelectrodes
        self.electrodes = [QtGui.QLCDNumber() for i in range(self.Nelectrodes)]
        
        elecLayout = QtGui.QGridLayout()
                
        for j in range(self.Nelectrodes/2):
            elecLayout.addWidget(QtGui.QLabel(str(j+1)),j,0)
            elecLayout.addWidget(self.electrodes[j],j,1)
        for j in range(self.Nelectrodes/2,self.Nelectrodes-1):
            elecLayout.addWidget(QtGui.QLabel(str(j+1)), j - self.Nelectrodes/2,2)
            elecLayout.addWidget(self.electrodes[j],j - self.Nelectrodes/2,3)   

        elecLayout.addWidget(QtGui.QLabel('CNT'),int(round(self.Nelectrodes/2.))-1,2)
        elecLayout.addWidget(self.electrodes[self.Nelectrodes-1], int(round(self.Nelectrodes/2.)) - 1,3) 

        self.setLayout(elecLayout)      
        
    @inlineCallbacks
    def connect(self):
        from labrad.wrappers import connectAsync
        from labrad.types import Error
        self.cxn = yield connectAsync()
        self.dacserver = yield self.cxn.cctdac_pulser
        yield self.setupListeners()
        
    @inlineCallbacks    
    def setupListeners(self):
        yield self.dacserver.signal__ports_updated(SIGNALID2)
        yield self.dacserver.addListener(listener = self.followSignal, source = None, ID = SIGNALID2)
    
    @inlineCallbacks
    def followSignal(self, x, s):
        print "CHMON followSignal"
        av = yield self.dacserver.get_analog_voltages()
        for (e, v) in zip(self.electrodes, av):
            e.display(float(v))
        for (i, v) in zip(range(self.Nelectrodes), av):
            if math.fabs(v) > 10:
                self.electrodes[i].setStyleSheet("QWidget {background-color: orange }")
                self.electrodes[i].setAutoFillBackground(True)
            if math.fabs(v) < 10:
                self.electrodes[i].setStyleSheet("QWidget {background-color:  }")
                self.electrodes[i].setAutoFillBackground(False)      
       
    def closeEvent(self, x):
        self.reactor.stop()

class DAC_CONTROL(QtGui.QMainWindow):
    def __init__(self, reactor, parent=None):
        super(DAC_CONTROL, self).__init__(parent)
        
        self.reactor = reactor
        self.Nelectrodes = 18

        channelControlTab = self.buildChannelControlTab()        
        multipoleControlTab = self.buildMultipoleControlTab()
        tabWidget = QtGui.QTabWidget()
        tabWidget.addTab(multipoleControlTab,'&Multipoles')
        tabWidget.addTab(channelControlTab, '&Channels')
        self.setCentralWidget(tabWidget)
    
    def buildMultipoleControlTab(self):
        widget = QtGui.QWidget()
        gridLayout = QtGui.QGridLayout()
        gridLayout.addWidget(CHANNEL_MONITOR(self.reactor, self.Nelectrodes),0,0)
        gridLayout.addWidget(MULTIPOLE_CONTROL(self.reactor),0,1)
        widget.setLayout(gridLayout)
        return widget

    def buildChannelControlTab(self):
        widget = QtGui.QWidget()
        gridLayout = QtGui.QGridLayout()
        gridLayout.addWidget(CHANNEL_CONTROL(self.reactor),0,0)
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
