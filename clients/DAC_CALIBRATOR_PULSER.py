import sys
from PyQt4 import QtGui
from PyQt4 import QtCore,uic
from qtui.QDACCalibrator import QDACCalibrator
import time
import numpy as np
import matplotlib.pyplot as plt
import datetime
from random import randrange as r

class DAC_CALIBRATOR(QDACCalibrator):
    def __init__(self, cxncam, cxn, parent=None):
        self.dacserver = cxn.cctdac_pulser
        self.dmmserver = cxncam.keithley_2100_dmm
        self.datavault = cxn.data_vault
        self.registry = cxn.registry

        QDACCalibrator.__init__(self, parent)

        self.clicked = False # state of the "Calibrate" button
        self.start.released.connect(self.buttonClicked)
            

    # This is where the magic happens
    def calib(self):
        now = datetime.datetime.now()
        date = now.strftime("%Y%m%d")
        TIME = now.strftime('%H%M%S')      
        
        self.datavault.cd(['', date, 'Calibrations',str(self.channelToCalib) + TIME], True)
        self.datavault.new(str(self.channelToCalib) + TIME,[('digital', '')], [('Analog', 'Volts', 'Volts')])
        self.datavault.add_parameter('plotLive',True)
	
        
        #stepsize = 0b101010101

        stepsize = 1000
        self.numSteps = (61000-5000)/stepsize        
        self.digVoltages = [ 5000 + r(0, stepsize) + i*stepsize for i in  range(self.numSteps)]
        self.compareVolts = [ 5000 + r(0, stepsize) + i*stepsize for i in  range(self.numSteps)]
            

        #self.digVoltages = range(0, 2**16, stepsize) # digital voltages we're going to iterate over
        self.anaVoltages = [] # corresponding analog voltages in volts
        self.dacserver.set_individual_digital_voltages([(int(self.channelToCalib), self.digVoltages[0])], 1)
        time.sleep(.3)
        for dv in self.digVoltages: # iterate over digital voltages

            self.dacserver.set_individual_digital_voltages([(int(self.channelToCalib), dv)], 1) 

            time.sleep(.3)
            
            av = self.dmmserver.get_dc_volts()
            #av = 0

            self.anaVoltages.append(av)
            self.datavault.add(dv, av)
            print dv, "; ", av
        
#        plt.figure(1)
#        plt.plot(self.digVoltages, self.anaVoltages, 'ro')
#        plt.show()

        fit = np.polyfit(self.anaVoltages, self.digVoltages, 3) # fit to a second order polynomial
        if self.checksave.isChecked():
            self.registry.cd(['', 'cctdac_pulser', 'Calibrations'])
            #self.registry.mkdir(str(self.channelToCalib))
            self.registry.cd(['', 'cctdac_pulser', 'Calibrations', str(self.channelToCalib)])
            self.registry.set('c0', fit[3])
            self.registry.set('c1', fit[2])
            self.registry.set('c2', fit[1])
            self.registry.set('c3', fit[0])
    
        return fit

    def buttonClicked(self):
        self.channelToCalib = str(self.port.text())
        print self.channelToCalib
        
        self.clicked = True
        fit = self.calib() # Now calibrate
        self.results.setText('RESULTS')
        self.y_int.setText('Intercept: ' + str(fit[2]))
        self.slope.setText('Slope: ' + str(fit[1]))
        self.order2.setText('Nonlinearity: ' + str(fit[0]))
        
        fitvals = np.array([ v*v*v*fit[0] + v*v*fit[1] + v * fit[2] + fit[3] for v in self.anaVoltages])
        diffs = fitvals - self.digVoltages

        m = 80./(2**16 - 1)
        b = -40
        idealVals = np.array([m*v + b for v in self.digVoltages])
        uncalDiffs = idealVals - self.anaVoltages
        
        print "MAX DEVIATION: ", max(abs(diffs)), " bits, or ~", m*max(abs(diffs))*1000., " mV"
#        plt.figure(2)
#        plt.plot(self.digVoltages, 1000*(diffs))
#        plt.title('Actual deviation from fit (mV)')
#        plt.figure(3)
#        plt.plot(self.digVoltages, 1000*(uncalDiffs) )
#        plt.title('Deviation from nominal settings (mV)')
#        plt.show()
        
#        print "MAX DEV FROM NOMINAL: ", max(abs(uncalDiffs)), " bits"

if __name__=="__main__":
    import labrad
    cxn = labrad.connect()
    cxncam = labrad.connect('192.168.169.30')
    dacserver = cxn.cctdac_pulser
    dmmserver = cxncam.keithley_2100_dmm
    dmmserver.select_device('GPIB Bus - USB0::0x05E6::0x2100::1243106')
    app = QtGui.QApplication(sys.argv)
    icon = DAC_CALIBRATOR(cxncam, cxn)
    icon.show()
    app.exec_()
