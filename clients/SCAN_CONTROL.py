import sys;
sys.path.append('/home/cct/LabRAD/cct/scripts/simpleMeasurements/FFT')
import os
from PyQt4 import QtGui
from PyQt4 import QtCore,uic
import numpy
import datetime
import time as TIME
from twisted.internet.defer import inlineCallbacks, returnValue

DminAmp = -0.1
DmaxAmp = 0.1
DsizeStepsAmp = .01
DnumStepsAmp = (DmaxAmp - DminAmp)/DsizeStepsAmp
Davg = 6
DminTfrq = 40
DmaxTfrq = 50
DsizeStepsTfrq = .5
DnumStepsTfrq = (DmaxTfrq - DminTfrq)/DsizeStepsTfrq

class SCAN(QtGui.QWidget):
    def __init__(self, reactor, axis, parent=None):
        super(SCAN, self).__init__(parent)
        self.axis = axis
        self.running = False
        self.reactor = reactor
        self.makeGUI()
        self.connect()

    def makeGUI(self):
        axis = self.axis
        layout = QtGui.QGridLayout()
        groupBox = QtGui.QGroupBox('Scan %s Tickle' % axis[:2])
        groupBoxLayout = QtGui.QGridLayout()
        self.controlLabels = ['minAmp', 'maxAmp', 'numStepsAmp', 'sizeStepsAmp', 'avg', 'minTfrq', 'maxTfrq', 'numStepsTfrq', 'sizeStepsTfrq' ]
        self.control = {}
        for label in self.controlLabels:
            self.control[label] = QtGui.QDoubleSpinBox()
            self.control[label].setDecimals(4)
        self.label = {}	
        self.button = {}
        self.control['minAmp'].setRange(-10,10)
        self.control['minAmp'].setValue(DminAmp)
        self.label['minAmp'] = QtGui.QLabel('minimum %s [V/m]:' % axis[:2])
        self.control['maxAmp'].setRange(-10, 10)
        self.control['maxAmp'].setValue(DmaxAmp)
        self.label['maxAmp'] = QtGui.QLabel('maximum %s [V/m]:' % axis[:2])
        self.control['numStepsAmp'].setValue(DnumStepsAmp)
        self.label['numStepsAmp'] = QtGui.QLabel('number of %s steps:' % axis[:2])
        self.control['sizeStepsAmp'].setValue(DsizeStepsAmp)
        self.label['sizeStepsAmp'] = QtGui.QLabel('%s step size [V/m]:' % axis[:2])
        self.control['avg'].setValue(Davg)
        self.control['avg'].setDecimals(0)
        self.label['avg'] = QtGui.QLabel('number to average:')
        self.control['minTfrq'].setValue(DminTfrq)
        self.label['minTfrq'] = QtGui.QLabel('minimum tickle frq [MHz]:')
        self.control['maxTfrq'].setValue(DmaxTfrq)
        self.label['maxTfrq'] = QtGui.QLabel('maximum tickle frq [MHz]:')
        self.control['numStepsTfrq'].setValue(DnumStepsTfrq)
        self.label['numStepsTfrq'] = QtGui.QLabel('number of tickle steps:')
        self.control['sizeStepsTfrq'].setValue(DsizeStepsTfrq)
        self.label['sizeStepsTfrq'] = QtGui.QLabel('tickle step size:')
        self.button['scan'] = QtGui.QPushButton('Scan')
        self.button['stop'] = QtGui.QPushButton('Stop')
        self.button['revAmp'] = QtGui.QCheckBox('reverse')
        self.button['revT'] = QtGui.QCheckBox('reverse')
        groupBox.setLayout(groupBoxLayout)
        layout.addWidget(groupBox, 0, 0)
        for i, l in enumerate(self.controlLabels):
            groupBoxLayout.addWidget(self.control[l], i, 1)
            groupBoxLayout.addWidget(self.label[l], i, 0)
        groupBoxLayout.addWidget(self.button['scan'], len(self.controlLabels) + 1, 0, 1, 2)
        groupBoxLayout.addWidget(self.button['stop'], len(self.controlLabels) + 2, 0, 1, 2)
        groupBoxLayout.addWidget(self.button['revAmp'], 3, 2)
        groupBoxLayout.addWidget(self.button['revT'], 8, 2)
        self.setLayout(layout)

    @inlineCallbacks
    def connect(self):
        from labrad.wrappers import connectAsync
        from labrad.types import Error
        from labrad import types as T
        self.T = T
        self.cxn = yield connectAsync()
        self.cxncam = yield connectAsync('192.168.169.30')
        self.r = yield self.cxn.registry
        self.dv = yield self.cxn.data_vault
        self.ds = yield self.cxn.cctdac_pulser_v2
        self.pmt = self.cxn.normalpmtflow
        self.rs = self.cxncam.rohdeschwarz_server
        self.rs.select_device('cct_camera GPIB Bus - USB0::0x0AAD::0x0054::104543')
        self.control['numStepsAmp'].valueChanged.connect(self.numAStepsChanged)
        self.control['sizeStepsAmp'].valueChanged.connect(self.sizeAStepsChanged)
        self.control['numStepsTfrq'].valueChanged.connect(self.numTStepsChanged)
        self.control['sizeStepsTfrq'].valueChanged.connect(self.sizeTStepsChanged)
        self.button['scan'].clicked.connect(self.scan)
        self.button['stop'].clicked.connect(self.stopScan)
        self.r.cd('', 'Scan Control', self.axis[:2])
        for k in self.control.keys():
            last = yield self.r.get(k + self.axis[:2])
            self.control[k].setValue(last)
        
    def numAStepsChanged(self):
        if self.control['numStepsAmp'].value() == 0:
            return
        newSize = round((self.control['maxAmp'].value() - self.control['minAmp'].value())/self.control['numStepsAmp'].value(), 4)
        self.control['sizeStepsAmp'].setValue(newSize)

    def sizeAStepsChanged(self):
        if self.control['sizeStepsAmp'].value() == 0:
            return
        newNum = round((self.control['maxAmp'].value() - self.control['minAmp'].value())/self.control['sizeStepsAmp'].value(), 4)
        self.control['numStepsAmp'].setValue(newNum)

    def numTStepsChanged(self):
        if self.control['numStepsTfrq'].value() == 0:
            return
        newSize = round((self.control['maxTfrq'].value() - self.control['minTfrq'].value())/self.control['numStepsTfrq'].value(), 4)
        self.control['sizeStepsTfrq'].setValue(newSize)	

    def sizeTStepsChanged(self):
        if self.control['sizeStepsTfrq'].value() == 0:
            return
        newNum = round((self.control['maxTfrq'].value() - self.control['minTfrq'].value())/self.control['sizeStepsTfrq'].value(), 4)
        self.control['numStepsTfrq'].setValue(newNum)

    @inlineCallbacks
    def scan(self, c):
        axis = self.axis
        self.button['scan'].setText('Scan is running')
        self.running = True
        yield self.rs.output(True)
        now = datetime.datetime.now()
        date = now.strftime("%Y-%m-%d")
        time = now.strftime('%H%M%S')

        # add values to registry
        r = self.r
        r.cd(['', 'Scan Control', axis[:2]], True)
        for k in self.control.keys():
            r.set(k + axis[:2], self.control[k].value())

        amplitudes = numpy.arange(self.control['minAmp'].value(), self.control['maxAmp'].value(), self.control['sizeStepsAmp'].value())
        if self.button['revAmp'].isChecked():
            amplitudes = amplitudes[::-1]

        mv = yield self.ds.get_multipole_values()
        D = {}
        for v in mv:
            D[v[0]] = v[1]
        initA = D[axis]
        del D[axis]
        for A in amplitudes:
            yield self.rs.output(True)
            dirName = time + '-%s and Tickle' % axis[:2]
            yield self.dv.cd(['', date,'MMComp', dirName],True)
            graphName = axis[:2] + ': ' + str(A)
            name = yield self.dv.new(graphName,[('Frequency', 'Hz')], [('PMT Counts', 'PMT counts', 'PMT counts')])
            yield self.dv.add_parameter(axis[:2], A)
            yield self.dv.add_parameter('plotLive',True)
            print 'Saving {}'.format(name)
            yield self.ds.set_multipole_values([(v, D[v]) for v in D.keys()] + [(axis, A)])
            print "Set multipole values"
            frequencies = numpy.arange(self.control['minTfrq'].value(), self.control['maxTfrq'].value(), self.control['sizeStepsTfrq'].value())
            if self.button['revT'].isChecked():	
                frequencies = frequencies[::-1] # The ion asks that you kindly scan downwards, thanks
            for f in frequencies:
                if self.running == False:
                    yield self.rs.output(False)
                    yield self.ds.set_multipole_values([(v, D[v]) for v in D.keys()] + [(axis, initA)])
                    self.button['scan'].setText('Scan')
                    return
                self.rs.frequency(self.T.Value(f, 'MHz'))
                print "set the frequency"
                #TIME.sleep(.3)
                pmtcount = yield self.pmt.get_next_counts('ON', int(self.control['avg'].value()), True)	
                print pmtcount
                yield self.dv.add(f, pmtcount)
            yield self.rs.output(False)
            yield self.ds.set_multipole_values([(v, D[v]) for v in D.keys()] + [(axis, initA)])
            self.button['scan'].setText('Scan')

    def stopScan(self, c):
        self.running = False

    def closeEvent(self, x):
        self.reactor.stop()
        
class Scan_Control_Tickle(QtGui.QMainWindow):
    def __init__(self, reactor, axis, parent=None):
        super(Scan_Control_Tickle, self).__init__(parent)
        self.axis = axis
        self.reactor = reactor
        W = self.buildW(reactor)
        widget = QtGui.QWidget()
        gridLayout = QtGui.QGridLayout()
        gridLayout.addWidget(W, 0, 0)
        self.setWindowTitle('Scan %s and Tickle Control' % axis[:2])
        widget.setLayout(gridLayout)
        self.setCentralWidget(widget)

    def buildW(self, reactor):
        W = QtGui.QWidget()
        subLayout = QtGui.QGridLayout()
        subLayout.addWidget(SCAN(reactor, self.axis), 0, 0)
        W.setLayout(subLayout)
        return W
                
    def closeEvent(self, x):
        self.reactor.stop()
        
if __name__=="__main__":
    a = QtGui.QApplication( [] )
    import qt4reactor
    qt4reactor.install()
    from twisted.internet import reactor
    Scan_Control_Tickle = Scan_Control_Tickle(reactor, 'Ex1')
    Scan_Control_Tickle.show()
    reactor.run() 
