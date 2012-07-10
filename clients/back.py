import sys
import os
from PyQt4 import QtGui
from PyQt4 import QtCore,uic
from numpy import *
from qtui.QDACControl import QDACControl
from qtui.QCustomLevelSpin import QCustomLevelSpin
from qtui.QCustomLevelTilt import QCustomLevelTilt
#import labrad

from twisted.internet.defer import inlineCallbacks, returnValue

UpdateTime = 100 # ms

class XYpos (QtGui.QWidget):
    def __init__(self, reactor, axis, parent=None):
        super(XYpos, self).__init__(parent)
        self.reactor = reactor
        self.connect()
        
        ctrlLayout = QtGui.QGridLayout()
        
        self.label = str(axis)
        
        self.delta = {}
        self.delta[self.label] = QtGui.QDoubleSpinBox()
        self.delta[self.label].setRange (0., 25.) 
        self.delta[self.label].setSingleStep (.01)
        self.delta[self.label].setDecimals (6)
        
        self.control = {}
        self.control[self.label] = QtGui.QDoubleSpinBox()
        self.control[self.label].setRange (0., 25.) 
        self.control[self.label].setSingleStep (.01)
        self.control[self.label].setDecimals (6)
        

   
        self.position = {}
        self.position[self.label] = 0
        


        ctrlLayout.addWidget(self.control[self.label],0,0)
        ctrlLayout.addWidget(self.delta[self.label], 1, 0)

        self.inputUpdated = False                
        self.timer = QtCore.QTimer(self)        
        self.timer.timeout.connect(self.sendToServer)
        self.timer.start(UpdateTime)
        
        self.control[self.label].valueChanged.connect(self.inputHasUpdated(self.label))
        
        self.setLayout(ctrlLayout)
        
    @inlineCallbacks
    def connect(self):
        from labrad.wrappers import connectAsync
        from labrad.types import Error
        self.cxn = yield connectAsync()
        self.stageserver = yield self.cxn.cctmain_sst

    def inputHasUpdated(self, label):
        def iu():
            self.inputUpdated = True
            print "in inputHasUpdated"
            self.position[self.label] = round(self.control[self.label].value(), 6)
        return iu
    
    def sendToServer(self):
        if self.inputUpdated:
            self.stageserver.move_abs( self.label, self.position[self.label]) 
            #self.stageserver.move_abs([(self.label, self.position[self.label])])
            print "set value"
            self.inputUpdated = False
#   
#    @inlineCallbacks    
#    def setupListeners(self):
#        yield self.stageserver.signal__ports_updated(SIGNALID2)
#        yield self.stageserver.addListener(listener = self.followSignal, source = None, ID = SIGNALID2)
#    
#    @inlineCallbacks
#    def followSignal(self, x, s):
#        av = yield self.stageserver.get_analog_voltages()
#        for (c, v) in zip(self.controlLabels, av):
#            self.controls[c].setValueNoSignal(v)
#        
    def closeEvent(self, x):
        self.reactor.stop()   

class arrows (QtGui.QWidget):
    def __init__(self, reactor, parent=None):
        super(arrows, self).__init__(parent)
        self.reactor = reactor
        self.connect()
        
        ctrlLayout = QtGui.QGridLayout()
        
        self.labels = ['posx', 'negx', 'posy', 'negy']
        
        self.button = {}
        for label in self.labels:
            self.button[label] = QtGui.QPushButton(label)
    
        ctrlLayout.addWidget(self.button['posx'],1,2)
        ctrlLayout.addWidget(self.button['negx'],1,0)
        ctrlLayout.addWidget(self.button['posy'],0,1)
        ctrlLayout.addWidget(self.button['negy'],2,1)  
       
        self.L2 = ['x', 'y']
        self.delta = {}
        for label in self.L2:
            self.delta[label] = QtGui.QDoubleSpinBox()

        
        ctrlLayout.addWidget(self.delta['x'], 3, 0)
        ctrlLayout.addWidget(self.delta['y'], 3, 2)
        
        self.inputUpdated = False                
        self.timer = QtCore.QTimer(self)        
        self.timer.timeout.connect(self.sendToServer)
        self.timer.start(UpdateTime)
        
        for label in self.labels:
            self.button[label].released.connect(self.inputHasUpdated(label))
            
        self.setLayout(ctrlLayout)
    
    
    def labelToAxis(self, label):
        axis = label[3:]
        return str(axis)
                       
    @inlineCallbacks
    def connect(self):
        from labrad.wrappers import connectAsync
        from labrad.types import Error
        self.cxn = yield connectAsync()
        self.stageserver = yield self.cxn.cctmain_sst
        
    def inputHasUpdated(self, label):
        def iu():
            self.inputUpdated = True
            self.changedAxis = self.labelToAxis(label)
        return iu
    
    def sendToServer(self):
        if self.inputUpdated:
            axis = self.changedAxis
            change = self.delta[axis]
            self.stageserver.move_rel( axis, change)
            self.inputUpdated = False

    def closeEvent(self, x):
        self.reactor.stop()   
        
        
class STAGE_CONTROL(QtGui.QMainWindow):
    def __init__(self, reactor, parent=None):
        super(STAGE_CONTROL, self).__init__(parent)
        
        self.reactor = reactor
        widget = QtGui.QWidget()
        gridLayout = QtGui.QGridLayout()
        top = self.makeTopWidget
        wid
#        gridLayout.addWidget(arrows(reactor), 1, 0)
        
        widget.setLayout(gridLayout) 
        self.setCentralWidget(widget) 
        
    def makeTopWidget(self, reactor):
        widget = QtGui.QWidget()
        import XYpos
        gridLayout = QtGui.QGridLayout()
        gridLayout.addWidget(XYpos(reactor, 'x'),0,0)
        gridLayout.addWidget(XYpos(reactor, 'y'),0,1)        
        widget.setLayout(gridLayout)
        return widget
                
    def closeEvent(self, x):
        self.reactor.stop() 
         
if __name__ == "__main__":
    a = QtGui.QApplication( [] )
    import qt4reactor
    qt4reactor.install()
    from twisted.internet import reactor
    STAGE_CONTROL = STAGE_CONTROL(reactor)
    STAGE_CONTROL.show()
    reactor.run()
