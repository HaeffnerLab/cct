import sys
import os
from PyQt4 import QtGui
from PyQt4 import QtCore,uic
from twisted.internet.defer import inlineCallbacks, returnValue


UpdateTime = 100 # ms
StateTime = 1000
DEFAULTSTEP = .1
DEFAULTx1 = 0
DEFAULTx2 = 0
DEFAULTy1 = 0
DEFAULTy2 = 0
        
class XYpos (QtGui.QWidget):
    def __init__(self, reactor, parent=None):
        super(XYpos, self).__init__(parent)
        self.reactor = reactor
        self.connect()
        
        ctrlLayout = QtGui.QGridLayout()
        
        self.labels = ['x1', 'y1', 'x2', 'y2']
    
        self.control = {}
        for label in self.labels:
            self.control[label] = QtGui.QDoubleSpinBox()
            self.control[label].setRange (0., 25.) 
            self.control[label].setSingleStep (DEFAULTSTEP)
            self.control[label].setDecimals (6)
            self.control[label].setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
            self.control[label].setSuffix(' mm')
        self.control['y1'].setPrefix('-')
        self.control['y2'].setPrefix('-')  
        
        self.control['x1'].setValue(DEFAULTx1)
        self.control['y1'].setValue(DEFAULTy1)
        self.control['x2'].setValue(DEFAULTx2)
        self.control['y2'].setValue(DEFAULTy2)      

        self.delta = {}
        for label in self.labels:        
            self.delta[label] = QtGui.QDoubleSpinBox()
            self.delta[label].setRange (0., 5.) 
            self.delta[label].setSingleStep (.001)
            self.delta[label].setDecimals (6)
            self.delta[label].setValue(DEFAULTSTEP)
            self.delta[label].setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        
        self.position = {}
        self.position['x1'] = DEFAULTx1
        self.position['y1'] = DEFAULTy1
        self.position['x2'] = DEFAULTx2
        self.position['y2'] = DEFAULTy2

        for x in self.labels:
            self.updatedControl = x
            self.control[x].setValue(self.position[x])

        ctrlLayout.addWidget(self.control['x1'],1,0)
        ctrlLayout.addWidget(self.control['y1'],1,2)
        ctrlLayout.addWidget(self.control['x2'],1,3)
        ctrlLayout.addWidget(self.control['y2'],1,5)
        ctrlLayout.addWidget(self.delta['x1'], 5, 0)
        ctrlLayout.addWidget(self.delta['y1'], 5, 2)
        ctrlLayout.addWidget(self.delta['x2'], 5, 3)
        ctrlLayout.addWidget(self.delta['y2'], 5, 5)   
        

        self.arrowLabels = ['posx1', 'negx1', 'posy1', 'negy1', 'posx2', 'negx2', 'posy2', 'negy2']

        self.button = {}
        self.button['posx1'] = QtGui.QPushButton('>')
        self.button['negx1'] = QtGui.QPushButton('<')
        self.button['posy1'] = QtGui.QPushButton('v')    #switched b/c y stage 0 is highest point
        self.button['negy1'] = QtGui.QPushButton('^')
        self.button['posx2'] = QtGui.QPushButton('>')
        self.button['negx2'] = QtGui.QPushButton('<')
        self.button['posy2'] = QtGui.QPushButton('v')
        self.button['negy2'] = QtGui.QPushButton('^')
        
        
        self.sendButton = {}
        self.sendButton['x1'] = QtGui.QPushButton('Send x1')
        self.sendButton['y1'] = QtGui.QPushButton('Send y1')
        self.sendButton['x2'] = QtGui.QPushButton('Send x2')
        self.sendButton['y2'] = QtGui.QPushButton('Send y2')
    
        ctrlLayout.addWidget(self.button['posx1'],3,2)
        ctrlLayout.addWidget(self.button['negx1'],3,0)
        ctrlLayout.addWidget(self.button['posy1'],4,1)
        ctrlLayout.addWidget(self.button['negy1'],2,1)
        ctrlLayout.addWidget(self.button['posx2'],3,5)
        ctrlLayout.addWidget(self.button['negx2'],3,3)
        ctrlLayout.addWidget(self.button['posy2'],4,4)
        ctrlLayout.addWidget(self.button['negy2'],2,4)
        ctrlLayout.addWidget(self.sendButton['x1'],2,0)
        ctrlLayout.addWidget(self.sendButton['y1'],2,2)
        ctrlLayout.addWidget(self.sendButton['x2'],2,3)
        ctrlLayout.addWidget(self.sendButton['y2'],2,5)
        

        ctrlLayout.addWidget(QtGui.QLabel(' x1 displacement'),0,0) 
        ctrlLayout.addWidget(QtGui.QLabel(' y1 displacement'),0,2)
        ctrlLayout.addWidget(QtGui.QLabel('   x1 step size'),6,0) 
        ctrlLayout.addWidget(QtGui.QLabel('   y1 step size'),6,2)
        ctrlLayout.addWidget(QtGui.QLabel(' x2 displacement'),0,3) 
        ctrlLayout.addWidget(QtGui.QLabel(' y2 displacement'),0,5)
        ctrlLayout.addWidget(QtGui.QLabel('   x2 step size'),6,3) 
        ctrlLayout.addWidget(QtGui.QLabel('   y2 step size'),6,5)
        
        self.controlInputUpdated = False
        self.buttonPushed = False
        self.startup = True
        
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.updatePosition)
        self.timer.start(UpdateTime)
        
        self.moving = {}
        for label in self.labels:
            self.moving[label] = False
        
        self.stateTimer = QtCore.QTimer(self)
        self.stateTimer.timeout.connect(self.updateState)
        self.stateTimer.start(StateTime)
        
        for label in self.labels:
            self.sendButton[label].clicked.connect(self.controlHasUpdated(label))

        for label in self.arrowLabels:
            self.button[label].clicked.connect(self.buttonWasPushed(label))

        self.setLayout(ctrlLayout)
        

    
    @inlineCallbacks
    def connect(self):
        from labrad.wrappers import connectAsync
        from labrad.types import Error
        self.cxn = yield connectAsync()
        self.stageserver = yield self.cxn.cctmain_stage_server
                   
    def controlHasUpdated(self, label):
        def iu():
            self.controlInputUpdated = True
            self.position[label] = round(self.control[label].value(), 6)
            self.updatedControl = label
        return iu
    
    def buttonWasPushed(self, label):
        def iu():
            self.buttonPushed = True
            self.axis = label[3:]
            self.dirn = label[:3]
        return iu
            
    @inlineCallbacks 
    def updatePosition(self): 
        if self.buttonPushed:
            if self.dirn == 'pos':
                self.control[self.axis].setValue(float(self.control[self.axis].value() + self.delta[self.axis].value()))
            elif self.dirn == 'neg':
                newVal = (self.control[self.axis].value() - self.delta[self.axis].value()) 
                if newVal < 0: 
                    self.control[self.axis].setValue(0)
                else:    
                    self.control[self.axis].setValue(float(self.control[self.axis].value() - self.delta[self.axis].value()))
            self.controlInputUpdated = True
        self.buttonPushed = False
        yield self.sendToServer()  
    
    @inlineCallbacks    
    def sendToServer(self):
        if self.controlInputUpdated:
            yield self.stageserver.move_abs(self.updatedControl, self.position[self.updatedControl])
            self.moving[self.updatedControl] = True
        self.controlInputUpdated = False 
               
    @inlineCallbacks
    def updateState(self):
        for label in self.labels:
            if self.moving[label]:
                yield self.stageserver.ask_state(label)
                ready = yield self.stageserver.get_state(label)
                if ready == 0:
                    self.control[label].setStyleSheet("QWidget {background-color: orange }")
                    self.control[label].setAutoFillBackground(True)
                    self.control[label].setRange(self.position[label], self.position[label])
                else:
                    self.control[label].setStyleSheet("QWidget {background-color: }")
                    self.control[label].setAutoFillBackground(False)
                    self.control[label].setRange(0, 25.)
                    self.moving[label] = False                             
                    
    def closeEvent(self, x):
        self.reactor.stop()   

class STAGE_CONTROL(QtGui.QMainWindow):
    def __init__(self, reactor, parent=None):
        super(STAGE_CONTROL, self).__init__(parent)
        
        self.reactor = reactor
        widget = QtGui.QWidget()
        gridLayout = QtGui.QGridLayout()    
        gridLayout.addWidget(XYpos(reactor), 1, 0)
        self.setWindowTitle('Stage Control')
        widget.setLayout(gridLayout) 
        self.setCentralWidget(widget) 
                
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
