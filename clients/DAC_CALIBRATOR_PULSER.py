import sys
from PyQt4 import QtGui
from PyQt4 import QtCore,uic
from qtui.QDACCalibrator import QDACCalibrator
import time
import numpy as np
import matplotlib.pyplot as plt
import datetime

class DAC_CALIBRATOR(QDACCalibrator):
    def __init__(self, cxncam, cxn, parent=None):
        self.dacserver = cxn.cctdac_pulser
        self.dmmserver = cxncam.keithley_2100_dmm
        self.dat = cxn.data_vault
        self.registry = cxn.registry

        QDACCalibrator.__init__(self, parent)

        self.clicked = False # state of the "Calibrate" button

        # Connect functions
        # self.spinPower.valueChanged.connect(self.powerChanged)
        self.start.released.connect(self.buttonClicked)
            

    # This is where the magic happens
    def calib(self):
	now = datetime.datetime.now()
	date = now.strftime("%Y%m%d")
	TIME = now.strftime('%H%M%S')      
      
	self.dat.cd(['', date, 'Calibrations',str(self.channelToCalib) + TIME], True)
	self.dat.new(str(self.channelToCalib) + TIME,[('digital', '')], [('Analog', 'Volts', 'Volts')])
	self.dat.add_parameter('plotLive',True)
	
        
        #stepsize = 0b101010101

        stepsize = 1001

        #self.digVoltages = range(0, 2**16, stepsize) # digital voltages we're going to iterate over
        self.digVoltages = range(5000, 61000, stepsize)
        self.anaVoltages = [] # corresponding analog voltages in volts
        self.dacserver.reset_index()
        self.dacserver.set_individual_digital_voltages([(int(self.channelToCalib), self.digVoltages[0])])
        time.sleep(.3)
        for dv in self.digVoltages: # iterate over digital voltages

            self.dacserver.set_individual_digital_voltages([(int(self.channelToCalib), dv)]) 

            time.sleep(.3)
            
            av = self.dmmserver.get_dc_volts()
            #av = 0

            self.anaVoltages.append(av)
            self.dat.add(dv, av)
            print dv, "; ", av
        
        plt.figure(1)
        plt.plot(self.digVoltages, self.anaVoltages, 'ro')
        plt.show()

        fit = np.polyfit(self.anaVoltages, self.digVoltages, 3) # fit to a second order polynomial
        if self.checksave.isChecked():
	    self.registry.cd(['', 'cctdac_pulser', 'Calibrations'])
	    #self.registry.mkdir(str(self.channelToCalib))
	    self.registry.cd(['', 'cctdac_pulser', 'Calibrations', str(self.channelToCalib)])
	    self.registry.set('c0', fit[3])
	    self.registry.set('c1', fit[2])
	    self.registry.set('c2', fit[1])
	    self.registry.set('c3', fit[0])
        
        
        print fit
    
        return fit

    def buttonClicked(self):
        self.channelToCalib = str(self.port.text())
        print self.channelToCalib
        
        self.clicked = True
        fit = self.calib() # Now calibrate

        #fit = [ -6.87774335e-18, 6.05469803e-13, 3.05235677e-04, -1.00067658e+01]
        #fit = [ -7.59798451e-18 ,  7.42121115e-13 ,  3.05226445e-04 , -1.00065850e+01]
        #fit = [ -6.33002825e-18 ,  5.78910501e-13  , 3.05234325e-04,  -1.00066765e+01]
        self.results.setText('RESULTS')
        self.y_int.setText('Intercept: ' + str(fit[2]))
        self.slope.setText('Slope: ' + str(fit[1]))
        #self.order2.setText('Nonlinearity: ' + str(fit[0]))
        
        fitvals = np.array([ v*v*v*fit[0] + v*v*fit[1] + v * fit[2] + fit[3] for v in self.digVoltages])
        diffs = fitvals - self.anaVoltages
        
        m = 80./(2**16 - 1)
        b = -40
        idealVals = np.array([m*v + b for v in self.digVoltages])
        uncalDiffs = idealVals - self.anaVoltages
        
        print "MAX DEVIATION: ", 1000*max(abs(diffs)), " mV"
        plt.figure(2)
        plt.plot(self.digVoltages, 1000*(diffs))
        plt.title('Actual deviation from fit (mV)')
        plt.figure(3)
        plt.plot(self.digVoltages, 1000*(uncalDiffs) )
        plt.title('Deviation from nominal settings (mV)')
        plt.show()
        
        print "MAX DEV FROM NOMINAL: ", 1000*max(abs(uncalDiffs)), " mV"

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
