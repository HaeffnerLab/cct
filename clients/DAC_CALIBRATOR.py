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
    
    # This is where the magic happens
    def calib(self):
        
        stepsize = 1

        digVoltages = range(0, 2**16, stepsize) # digital voltages we're going to iterate over
        anaVoltages = [] # corresponding analog voltages in volts
        self.dacserver.set_digital_voltages([0]*18)
        time.sleep(1)
        for dv in digVoltages: # iterate over digital voltages

            self.dacserver.set_digital_voltages([dv]*18) # just set all the channels at once

            time.sleep(1)
            
            av = self.dmmserver.get_dc_volts()
            #av = 0

            anaVoltages.append(av)
            print dv, "; ", av
        

        plt.plot(digVoltages, anaVoltages, 'ro')
        plt.show()

        fit = np.polyfit(digVoltages, anaVoltages, 2) # fit to a second order polynomial
        
        print fit
    
        # Save the raw data to the datavault
        now = time.ctime()
        self.datavault.cd( ( ['DACCalibrations', self.channelToCalib], True ) )
        self.datavault.new( (now, [('Digital voltage', 'num')], [('Volts','Analog Voltage','v')]) )
        self.datavault.add( np.array([digVoltages, anaVoltages]).transpose().tolist() )

        # Update the registry with the new calibration
        self.r.cd( ( ['Calibrations', self.channelToCalib], True ) )
        self.r.set( ( 'y_int', fit[2] ) )
        self.r.set( ( 'slope', fit[1] ) )

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
