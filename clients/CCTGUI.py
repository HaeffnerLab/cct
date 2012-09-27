from PyQt4 import QtGui, QtCore

class cctGUI(QtGui.QMainWindow):
    def __init__(self, reactor, parent=None):
        super(cctGUI, self).__init__(parent)
        self.reactor = reactor

        lightControlTab = self.makeLightWidget(reactor)
        voltageControlTab = self.makeVoltageWidget(reactor)
        piezoControlTab = self.makePiezoWidget(reactor)        
        tabWidget = QtGui.QTabWidget()
        tabWidget.addTab(voltageControlTab,'&Trap Voltages')
        tabWidget.addTab(lightControlTab,'&Laser Room')
        tabWidget.addTab(piezoControlTab, '&Piezo')
        self.setWindowTitle('CCTGUI')
        self.setCentralWidget(tabWidget)

    def makeLightWidget(self, reactor):        
        from CAVITY_CONTROL import cavityWidget
        from multiplexer.MULTIPLEXER_CONTROL import multiplexerWidget
        widget = QtGui.QWidget()
        gridLayout = QtGui.QGridLayout()
        gridLayout.addWidget(multiplexerWidget(reactor),0,1)
        gridLayout.addWidget(cavityWidget(reactor),0,0)
        widget.setLayout(gridLayout)
        return widget
    
    def makePiezoWidget(self, reactor):
        widget = QtGui.QWidget()
        from PIEZO_CONTROL import PIEZO_CONTROL
        gridLayout = QtGui.QGridLayout()
        gridLayout.addWidget(PIEZO_CONTROL(reactor), 0, 0)
        gridLayout.setRowStretch(1, 1)
        gridLayout.setColumnStretch(1, 1)
        widget.setLayout(gridLayout)
        return widget
        
    def makeVoltageWidget(self, reactor):        
        from DAC_CONTROL import DAC_Control
        from PMT_CONTROL import pmtWidget
        from PMT_CONTROL2 import pmtWidget as pmtWidget2
        from TRAPDRIVE_CONTROL import TD_CONTROL
        from TICKLE_CONTROL import Tickle_Control
        from SHUTTER_CONTROLv2 import SHUTTER
        from PIEZO_CONTROL import PIEZO_CONTROL
        from multiplexer.MULTIPLEXER_CONTROL import multiplexerWidget
        from SCAN_Ex_and_TICKLE import Scan_Control_Ex_and_Tickle
        from SCAN_Ey_and_TICKLE import Scan_Control_Ey_and_Tickle
        widget = QtGui.QWidget()
        gridLayout = QtGui.QGridLayout()        
        gridLayout.addWidget(DAC_Control(reactor), 0, 0)            
        rightPanel = QtGui.QGridLayout()
        rightPanel.addWidget(pmtWidget(reactor), 0, 0)
#        rightPanel.addWidget(pmtWidget2(reactor), 1, 0)        
        bottomPanel = QtGui.QGridLayout()
        bottomPanel.addWidget(Tickle_Control(reactor), 1, 1)      
        bottomPanel.addWidget(TD_CONTROL(reactor), 1, 0)
        bottomPanel.addWidget(SHUTTER(reactor), 1, 2) 
        gridLayout.addLayout(rightPanel, 0, 1, 2, 1)          
        gridLayout.addLayout(bottomPanel, 1, 0)
        gridLayout.setRowStretch(0, 1)
        rightPanel.setRowStretch(2, 1)            
        widget.setLayout(gridLayout)
        return widget

    def closeEvent(self, x):
        self.reactor.stop()

if __name__=="__main__":
    a = QtGui.QApplication( [] )
    import qt4reactor
    qt4reactor.install()
    from twisted.internet import reactor
    cctGUI = cctGUI(reactor)
    cctGUI.show()
    reactor.run()
