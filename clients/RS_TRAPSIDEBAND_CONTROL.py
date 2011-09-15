import sys
from PyQt4 import QtGui
from PyQt4 import QtCore,uic
from qtui.QCustomFreqPower import QCustomFreqPower

'''
Uses a RS signal generator to add a variable sideband to the trap drive.
djg -- 08/03/11
'''

MinPower = -145 #dbM
MaxPower = 0
MinFreq = 1 #Mhz
MaxFreq = 60
UpdateTime = 100 #in ms, how often data is checked for communication with the server

class TRAPSIDEBAND_CONTROL(QCustomFreqPower):
    def __init__(self, server,parent=None):
        QCustomFreqPower.__init__( self, 'Trapdrive Sideband Generator', (MinFreq,MaxFreq), (MinPower,MaxPower), parent )
        self.server= server
        #connect functions
        self.spinPower.valueChanged.connect(self.powerChanged)
        self.spinFreq.valueChanged.connect(self.freqChanged) 
        self.buttonSwitch.toggled.connect(self.switchChanged)
        #set initial values
        initpower = server.GetPower()
        initfreq = float(server.GetFreq())
        initstate = server.GetState()
        self.spinPower.setValue(initpower)
        self.spinFreq.setValue(initfreq)
        self.buttonSwitch.setChecked(initstate)
        self.setText(initstate)
        #keeping track of what's been updated
        self.powerUpdated = False;
        self.freqUpdated = False;
        self.switchUpdated = False;
        #start timer
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.sendToServer)
        self.timer.start(UpdateTime)
        
    def powerChanged(self):
        self.powerUpdated = True;
	
    def freqChanged(self):
        self.freqUpdated = True;
	
    def switchChanged(self):
      self.switchUpdated = True
        	            
    #if inputs are updated by user, send updated values to server
    def sendToServer(self):
        if(self.powerUpdated):
            print 'Trapdrive Sideband Generator sending new power'
            self.server.SetPower(self.spinPower.value())
            self.powerUpdated = False
        if(self.freqUpdated):
            print 'Trapdrive Sideband Generator sending new frequency'
            self.server.SetFreq(self.spinFreq.value())
            self.freqUpdated = False
        if(self.switchUpdated):
            print 'Trapdrive Sideband Generator sending new button'
            self.server.SetState(int(self.buttonSwitch.isChecked()))
            self.switchUpdated = False

if __name__=="__main__":
    import labrad
    cxn = labrad.connect()
    server = cxn.cctmain_rs_server_traprive_sideband
    server = 3
    app = QtGui.QApplication(sys.argv)
    icon = TRAPSIDEBAND_CONTROL(server)
    icon.show()
    app.exec_()
