import sys
from PyQt4 import QtGui
from PyQt4 import QtCore,uic
from qtui.QDACCalibrator import QDACCalibrator
import time
import numpy as np
import matplotlib.pyplot as plt
import datetime

class DAC_CALIBRATOR(QDACCalibrator):
    def __init__(self, cxn, parent=None):
        self.dacserver = cxn.cctdac
        self.dmmserver = cxn.keithley_2100_dmm
        self.datavault = cxn.data_vault
        self.r = cxn.registry

        QDACCalibrator.__init__(self, parent)

        self.clicked = False # state of the "Calibrate" button

        # Connect functions
        # self.spinPower.valueChanged.connect(self.powerChanged)
        self.start.released.connect(self.buttonClicked)
        print self.checksave.isChecked()
        print self.checkreverse.isChecked()
        print self.customsave.isChecked()
    # This is where the magic happens
    def calib(self):
        
        #stepsize = 0b101010101
        stepsize = 501
        reverserange = False
        #self.digVoltages = range(0, 2**16, stepsize) # digital voltages we're going to iterate over
        if self.checkreverse.isChecked() == False:
            self.digVoltages = range(0, 2**16, stepsize)
            print 'normal Voltage Scan'
        else:
            self.digVoltages = range(2**16,0, -stepsize)
            print 'inverted Voltage Scan'
        self.anaVoltages = [] # corresponding analog voltages in volts
        self.dacserver.set_individual_digital_voltages([(int(self.channelToCalib), 0)])
        #time.sleep(1)
        for dv in self.digVoltages: # iterate over digital voltages

            self.dacserver.set_individual_digital_voltages([(int(self.channelToCalib), dv)]) 
            print int(self.channelToCalib)
 
            time.sleep(.8)
            
            av = self.dmmserver.get_dc_volts()

            time.sleep(.2)
            #av = 0

            self.anaVoltages.append(av)
            print dv, "; ", av
        
        plt.figure(1)
        plt.plot(self.anaVoltages,self.digVoltages, 'ro')
        plt.show()

        fit = np.polyfit(self.anaVoltages,self.digVoltages, 2) # fit to a third order polynomial, where the output is the highest order coefficient first
        
        print fit
        
        # Save the raw data to the datavault
        if self.checksave.isChecked() == True:         
            now = time.ctime()
            self.datavault.cd( ( ['Calibrations', self.channelToCalib], True ) )
            self.datavault.new( (now, [('Digital voltage', 'num')], [('Volts','Analog Voltage','v')]) )
            self.datavault.add( np.array([self.digVoltages, self.anaVoltages]).transpose().tolist() )
            self.datavault.cd( ( [''] ))
            
            print 'stored to data vault: DACCalibrations Channel'+str(self.channelToCalib)
            # Update the registry with the new calibration
            self.r.cd( ( ['Calibrations', self.channelToCalib], True ) )
            self.r.set( ( 'c0', fit[2] ) )
            self.r.set( ( 'c1', fit[1] ) )
            self.r.set( ( 'c2', fit[0] ) )
            #self.r.set( ( 'c3', fit[0] ) )
            self.r.cd( ( [''] ))
            print 'Calibration stored in registry'
        else:
            print 'current Calibration NOT stored!'
        
        if self.customsave.isChecked() == True:
            now = time.ctime()
            self.datavault.cd( ( ['DACCalibrations', 'Channel_tests'], True ) )
            self.datavault.new( (str(now)+' - '+str(self.datainfo.text()), [('Digital voltage', 'num')], [('Volts','Analog Voltage','v')]) )
            self.datavault.add( np.array([self.digVoltages, self.anaVoltages]).transpose().tolist() )
            self.datavault.cd( ( [''] ))
            print 'Data set was stored separately as: '+str(now)+' - '+str(self.datainfo.text())
        else:
            print 'Data set was NOT stored separately!'
            
        return fit

        

    def buttonClicked(self):
        self.channelToCalib = str(self.port.text())
        print self.channelToCalib
        
        self.clicked = True
        fit = self.calib() # Now calibrate

        #fit = [ -6.87774335e-18, 6.05469803e-13, 3.05235677e-04, -1.00067658e+01]
        #fit = [ -7.59798451e-18 ,  7.42121115e-13 ,  3.05226445e-04 , -1.00065850e+01]
        #fit = [ -1.44425233e-17, 1.63743302e-12, 1.21768274e-03,-3.99139907e+01]
        #fit = [821.520125940606, 32777.0962644455]
        
        self.results.setText('RESULTS')
        self.y_int.setText('Intercept: ' + str(fit[2]))
        self.slope.setText('Slope: ' + str(fit[1]))
        self.order2.setText('Nonlinearity: ' + str(fit[0]))
        
        fitvals = np.array([ (v**2 * fit[0]) + (v * fit[1]) + fit[2] for v in self.anaVoltages])
        diffs = fitvals - self.digVoltages
        """
        m = 20./(2**16 - 1) #normal DAC output voltage range without any amplifiera
        b = -10
        idealVals = np.array([(m*v + b)*4 for v in self.digVoltages]) #factor four accounts for the amplifier +-40Volts
        uncalDiffs = idealVals - self.anaVoltages
        """
        print "MAX DEVIATION: ", max(abs(diffs)), " bits (1 digital step is 1.2mV"
        plt.figure(2)
        plt.plot(self.anaVoltages, (diffs))
        #plt.title('Actual deviation from fit (mV)')
        #plt.figure(4)
        #plt.plot(self.digVoltages, 1000*(uncalDiffs) )
        plt.title('Deviation from nominal settings (mV)')
        plt.figure(3)
        plt.plot(self.anaVoltages, self.digVoltages, 'ro')
        plt.plot(self.anaVoltages, fitvals)
        plt.show()
        
        #print "MAX DEV FROM NOMINAL: ", 1000*max(abs(uncalDiffs)), " mV"

if __name__=="__main__":
    import labrad
    cxn = labrad.connect()
    dacserver = cxn.cctdac
    dmmserver = cxn.keithley_2100_dmm
    datavault = cxn.data_vault
    registry = cxn.registry
    dmmserver.select_device('GPIB Bus - USB0::0x05E6::0x2100::1243106')
    app = QtGui.QApplication(sys.argv)
    icon = DAC_CALIBRATOR(cxn)
    icon.show()
    app.exec_()
