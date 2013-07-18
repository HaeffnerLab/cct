'''
flopalyzer.py

Take the FFT of a Rabi flop for finding the laser projection.
May be updated later to do more stuff.
'''

import numpy as np
from numpy import fft
import matplotlib.pyplot as plt
import labrad
from labrad import units as U
from labrad.units import hbar, amu

class Flopalyzer:

    def __init__(self, date, datasetname):
        self.date = date
        self.datasetname = datasetname
        data = self.get_data()
        self.time = self.data[:,0]
        self.excitation = self.data[:,1]
        self.freq, self.pos_freq_components = self.do_fft()
    
    def get_data(self):
        cxn = labrad.connect()
        dv = cxn.data_vault
        directory = ['', 'Experiments', 'RabiFlopping', self.date, self.datasetname]
        

        cxn.dv.cd(directory)
        cxn.dv.open(1)
        data = cxn.dv.get()


        sideband_selection = dv.get_parameter('RabiFlopping.sideband_selection')
        
        try:
            sideband_number = sideband_selection.index(1)
        except:
            print "Not a first order blue sideband! I can't figure out eta for you!"
            sideband_number = None

        if sideband_number is not None:
            sideband_list = ['TrapFrequencies.rf_drive_frequency',
                             'TrapFrequencies.axial_frequency', 
                             'TrapFrequencies.radial_frequency_1',
                             'TrapFrequencies.radial_frequency_2']

            sideband = sideband_list[sideband_number]
            self.trap_frequency = dv.get_parameter(sideband)
        
        return data.asarray

    def do_fft(self):
        tf = self.time[-1]
        n = len(self.excitation)
        x = fft.fft(self.excitation)
        pos_freq_components = x[1:n/2]
        freq = (np.arange(1,n/2)/tf)/1e3 # freq in kHz
        return freq, pos_freq_components
    
    def make_plots(self):
        plt.figure(1)
        plt.subplot(211)
        plt.plot(self.time,self.excitation)
        plt.subplot(212)
        plt.plot(self.freq,np.abs(self.pos_freq_components))
        plt.show()
    
    def compute_projection(self, bareRabi):
        '''
        May need a better peak detection algorithm in future
        '''
        try:
            wavelength = U.WithUnit(729.0, 'nm')
            m = 40*amu
            chi =  2*np.pi/wavelength['m']*np.sqrt(hbar['J*s']/(2.*m['kg']*2.*np.pi*self.trap_frequency['Hz']))
            freq_data = list(np.abs(self.pos_freq_components))        
            maxElemIndex = freq_data.index(max(freq_data))
            peakFreq = freq[maxElemIndex]*1e3 # freq in Hz
            theta = U.WithUnit( np.arccos(peakFreq/(chi*bareRabi['Hz']))*180.0/np.pi , 'deg' )
            return theta
        except:
            print "I already warned you that I can't compute your Lamb-Dicke parameter. You chose not to listen. Now look what you've done."
            return None

if __name__ == "__main__":

    bareRabi = U.WithUnit(56136.0, 'Hz')

    date = '2013Jul15'
    datasetname = '1549_31'

    f = Flopalyzer(date, datasetname)
    print "Projection: " + str(f.compute_projection(bareRabi))

    f.make_plots()
