import os
from PyQt4 import QtGui
from PyQt4 import QtCore,uic
from twisted.internet.defer import inlineCallbacks, returnValue

updateTime = 100

class SHUTTER (QtGui.QWidget):
    def __init__(self, reactor, parent=None):
        super(SHUTTER, self).__init__(parent)
        self.reactor = reactor
        self.connect()
        
        layout = QtGui.QGridLayout()
        self.labels = ['Blue PI', '866']
        self.state={}
        self.button = {}
        for l in self.labels:
            self.button[l] = QtGui.QPushButton()

        layout.addWidget(self.button['Blue PI'],0,0)
        layout.addWidget(self.button['866'],1,0)

        self.button['Blue PI'].clicked.connect(self.blueToggled)
        self.button['866'].clicked.connect(self.redToggled)
        
        self.setLayout(layout)

    @inlineCallbacks
    def connect(self):
        from labrad.wrappers import connectAsync
        cxn = yield connectAsync()
        self.pulser = cxn.pulser
        for label in self.labels:
            initState = yield self.pulser.get_state(self.ch(label))
            initState = initState[1]
            button = self.button[label]
            if initState:
                self.state[label] = 1
                button.setText(label + ': Open')
            else:
                self.state[label] = 0
                button.setText(label + ': Closed')
        
    def blueToggled(self):
        label = 'Blue PI'
        button = self.button[label]
        state = self.state[label]
        if state == 0:
            self.state[label] = 1
            button.setText(label + ': Open')
            self.pulser.switch_manual('bluePI', True)
        if state == 1:
            self.state[label] = 0
            button.setText(label + ': Closed')
            self.pulser.switch_manual('bluePI', False)    
            
    def redToggled(self):
        label = '866'
        button = self.button[label]
        state = self.state[label]
        if state == 0:
            self.state[label] = 1
            button.setText(label + ': Open')
            self.pulser.switch_manual('866', True)
        if state == 1:
            self.state[label] = 0
            button.setText(label + ': Closed')
            self.pulser.switch_manual('866', False)
            
    def ch(self, label):
        if label == 'Blue PI':
            return 'bluePI'
        if label == '866':
            return '866'
        
class SHUTTER_CONTROL(QtGui.QMainWindow):
    def __init__(self, reactor, parent=None):
        super(SHUTTER_CONTROL, self).__init__(parent)
        
        self.reactor = reactor
        widget = QtGui.QWidget()
        gridLayout = QtGui.QGridLayout()    
        gridLayout.addWidget(SHUTTER(self.reactor), 1, 0)
        self.setWindowTitle('Shutter Control')
        widget.setLayout(gridLayout) 
        self.setCentralWidget(widget) 
                
    def closeEvent(self, x):
        self.reactor.stop()

if __name__=="__main__":
    a = QtGui.QApplication( [] )
    import qt4reactor
    qt4reactor.install()
    from twisted.internet import reactor
    SHUTTER_CONTROL = SHUTTER_CONTROL(reactor)
    SHUTTER_CONTROL.show()
    reactor.run()

        
    
