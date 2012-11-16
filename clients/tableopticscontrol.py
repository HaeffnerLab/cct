# Control for table optics

from PyQt4 import QtGui, QtCore, uic
from qtui.SliderSpin import SliderSpin
from twisted.internet.defer import inlineCallbacks, returnValue

UpdateTime = 100 # ms
SIGNALID = 27883

class widgetWrapper():
    def __init__(self, displayName, freqRange):
        self.widget = None
        self.range = freqRange
        self.updated = False

    def makeWidget(self):
        self.widget = SliderSpin(self.displayName, 'MHz', self.freqRange, self.freqRange)

    def onUpdate(self):
        self.updated = True

class OPTICS_CONTROL(QtGui.QWidget):
    def __init__(self, reactor, parent=None):
        super(OPTICS_CONTROL, self).__init__(parent)

        self.reactor = reactor
        self.createDict()
        self.connect()
        
