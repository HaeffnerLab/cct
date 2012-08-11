from PyQt4 import QtGui, QtCore

class CCT_GUI(QtGui.QMainWindow):
    def __init__(self, reactor, parent=None):
        super(CCT_GUI, self).__init__(parent)
        self.reactor = reactor

        lightControlTab = self.makeLightWidget(reactor)
        voltageControlTab = self.makeVoltageWidget(reactor)

        tabWidget = QtGui.QTabWidget()
        tabWidget.addTab(voltageControlTab,'&Trap Voltages')
        tabWidget.addTab(lightControlTab,'&Laser Room')
        self.setWindowTitle('CCTGUI')

        self.setCentralWidget(tabWidget)

    def makeLightWidget(self, reactor):
        widget = QtGui.QWidget()
        from CAVITY_CONTROL import cavityWidget
        from multiplexer.MULTIPLEXER_CONTROL import multiplexerWidget
        gridLayout = QtGui.QGridLayout()
        gridLayout.addWidget(multiplexerWidget(reactor),0,1)
        gridLayout.addWidget(cavityWidget(reactor),0,0)
        gridLayout.setColumnStretch(1,5000)
        widget.setLayout(gridLayout)
        return widget

    def makeVoltageWidget(self, reactor):
        widget = QtGui.QWidget()
        from DAC_CONTROL import DAC_CONTROL
        from PMT_CONTROL import pmtWidget
        from PMT_CONTROL2 import pmtWidget as pmtWidget2
        from TRAPDRIVE_CONTROL import TD_CONTROL
        from TICKLE_CONTROL import Tickle_Control
        from SHUTTER_CONTROL import SHUTTER
        from PIEZO_CONTROL import PIEZO_CONTROL
        from multiplexer.MULTIPLEXER_CONTROL import multiplexerWidget
        from SCAN_Ex_and_TICKLE import Scan_Control_Ex_and_Tickle
        from SCAN_Ey_and_TICKLE import Scan_Control_Ey_and_Tickle
        gridLayout = QtGui.QGridLayout()
        subLayout = QtGui.QGridLayout()
        gridLayout.addWidget(DAC_CONTROL(reactor),0,0)
        gridLayout.addWidget(PIEZO_CONTROL(reactor),1,0)
        gridLayout.setColumnMinimumWidth(0,750)
        gridLayout.addLayout(subLayout,0,1, 2, 1)
        subLayout.addWidget(pmtWidget(reactor),0,0)
        subLayout.addWidget(pmtWidget2(reactor),1,0)
        subLayout.addWidget(Tickle_Control(reactor),2,0)      
        subLayout.addWidget(TD_CONTROL(reactor),3,0)
        subLayout.addWidget(SHUTTER(reactor), 4,0)               
        widget.setLayout(gridLayout)
        return widget

    def closeEvent(self, x):
        self.reactor.stop()

if __name__=="__main__":
    a = QtGui.QApplication( [] )
    import qt4reactor
    qt4reactor.install()
    from twisted.internet import reactor
    cctGUI = CCT_GUI(reactor)
    cctGUI.show()
    reactor.run()
