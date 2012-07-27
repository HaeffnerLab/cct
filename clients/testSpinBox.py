from PyQt4 import QtGui
from PyQt4 import QtCore,uic

class Test(QtGui.QWidget):
    def __init__(self, reactor, parent=None):
	super(Test,self).__init__(parent)
	self.reactor = reactor
	self.makeGUI()
	
    def makeGUI(self):
	onNewValues = QtCore.pyqtSignal()
	layout = QtGui.QGridLayout()
	groupBox = QtGui.QGroupBox('Test')
	groupBoxLayout = QtGui.QGridLayout()
	self.spinBox = QtGui.QDoubleSpinBox()
	groupBox.setLayout(groupBoxLayout)
	layout.addWidget(groupBox, 0, 0)	
	groupBoxLayout.addWidget(self.spinBox, 0, 0)
	self.spinBox.onNewValues.connect(self.pnt)
	self.setLayout(layout)

    def pnt(self):
	print self.spinBox.value()
	
    def closeEvent(self, x):
        self.reactor.stop()

class Test_Control(QtGui.QMainWindow):
    def __init__(self, reactor, parent=None):
        super(Test_Control, self).__init__(parent)
        self.reactor = reactor
        W = self.buildW(reactor)
        widget = QtGui.QWidget()
        gridLayout = QtGui.QGridLayout()    
        gridLayout.addWidget(W, 0, 0)
        self.setWindowTitle('test spinBox')
        widget.setLayout(gridLayout) 
        self.setCentralWidget(widget)

    def buildW(self, reactor):
        W = QtGui.QWidget()
        subLayout = QtGui.QGridLayout()
        subLayout.addWidget(Test(reactor), 0, 0)
        W.setLayout(subLayout)
        return W
                
    def closeEvent(self, x):
        self.reactor.stop()       
        
if __name__=="__main__":
    a = QtGui.QApplication( [] )
    import qt4reactor
    qt4reactor.install()
    from twisted.internet import reactor
    Test_Control = Test_Control(reactor)
    Test_Control.show()
    reactor.run()             