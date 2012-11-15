from PyQt4 import QtGui, QtCore
from twisted.internet.defer import inlineCallbacks, returnValue, Deferred

class cctGUI(QtGui.QMainWindow):
    def __init__(self, reactor, parent=None):
        super(cctGUI, self).__init__(parent)
        self.reactor = reactor
        self.connect_labrad()

    @inlineCallbacks
    def connect_labrad(self):
        from connection import connection
        cxn = connection()
        yield cxn.connect()
        self.create_layout(cxn)

    def create_layout(self, cxn):
        self.tabWidget = QtGui.QTabWidget()
        lightControlTab = self.makeLightWidget(reactor)
        voltageControlTab = self.makeVoltageWidget(reactor)
        piezoControlTab = self.makePiezoWidget(reactor)
        control729Widget = self.makecontrol729Widget(reactor, cxn)

        self.tabWidget.addTab(voltageControlTab,'&Trap Voltages')
        self.tabWidget.addTab(lightControlTab,'&Laser Room')
        self.tabWidget.addTab(piezoControlTab, '&Piezo')
        self.tabWidget.addTab(control729Widget, '&729 Control')
        
        scriptControl = self.makeScriptControl(reactor)

        self.createGrapherTab()
        
        gridLayout = QtGui.QGridLayout()
        gridLayout.addWidget(scriptControl, 0, 0, 1, 1)
        gridLayout.addWidget(self.tabWidget, 0, 1, 1, 3)
        centralWidget = QtGui.QWidget()
        centralWidget.setLayout(gridLayout)
        self.setCentralWidget(centralWidget)
        self.setWindowTitle('CCTGUI')


    def makeScriptControl(self, reactor):
        from guiscriptcontrol.scriptcontrol import ScriptControl
        self.sc = ScriptControl(reactor, self)
        self.sc, self.experimentParametersWidget = self.sc.getWidgets()
        self.createExperimentParametersTab()
        return self.sc

    def createExperimentParametersTab(self):
        self.tabWidget.addTab(self.experimentParametersWidget, '&Experiment Parameters')

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
        from SHUTTER_CONTROL import SHUTTER
        from PIEZO_CONTROL import PIEZO_CONTROL
        from multiplexer.MULTIPLEXER_CONTROL import multiplexerWidget
        widget = QtGui.QWidget()
        gridLayout = QtGui.QGridLayout()        
        gridLayout.addWidget(DAC_Control(reactor), 0, 0)            
        rightPanel = QtGui.QGridLayout()
        rightPanel.addWidget(pmtWidget(reactor), 0, 0)       
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
    
    @inlineCallbacks
    def createGrapherTab(self):
        grapherTab = yield self.makeGrapherWidget(reactor)
        self.tabWidget.addTab(grapherTab, '&Grapher')

    @inlineCallbacks
    def makeGrapherWidget(self, reactor):
        widget = QtGui.QWidget()
        from pygrapherlive.connections import CONNECTIONS
        vboxlayout = QtGui.QVBoxLayout()
        Connections = CONNECTIONS(reactor)
        @inlineCallbacks
        def widgetReady():
            window = yield Connections.introWindow
            vboxlayout.addWidget(window)
            widget.setLayout(vboxlayout)
        yield Connections.communicate.connectionReady.connect(widgetReady)
        returnValue(widget)

    def makecontrol729Widget(self, reactor, cxn):
        from control_729.control_729 import control_729
        widget = control_729(reactor, cxn)
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
