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
        self.time = data[:,0]
        self.excitation = data[:,1]
        self.freq, self.pos_freq_components = self.do_fft()
    
    def get_data(self):
        cxn = labrad.connect()
        dv = cxn.data_vault
        directory = ['', 'Experiments', 'RabiFlopping', self.date, self.datasetname]
        

        dv.cd(directory)
        dv.open(1)
        data = dv.get()


        sideband_selection = dv.get_parameter('RabiFlopping.sideband_selection')
        print sideband_selection
        try:
            sideband_number = sideband_selection.index(1)
            print sideband_number
        except:
            print "Not a first order blue sideband! I can't figure out eta for you!"
            sideband_number = None

        if sideband_number is not None:
            sideband_list = [                         
                             'TrapFrequencies.radial_frequency_1',
                             'TrapFrequencies.radial_frequency_2',
                             'TrapFrequencies.axial_frequency', 
                             'TrapFrequencies.rf_drive_frequency']

            sideband = sideband_list[sideband_number]
            print sideband
            self.trap_frequency = dv.get_parameter(sideband)
            print dv.get_parameter(sideband)
        return data.asarray

    def do_fft(self):
        tf = self.time[-1]*1e-6
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
        
        wavelength = U.WithUnit(729.0, 'nm')
        m = 40*amu
        chi =  2*np.pi/wavelength['m']*np.sqrt(hbar['J*s']/(2.*m['kg']*2.*np.pi*self.trap_frequency['Hz']))
        freq_data = list(np.abs(self.pos_freq_components))        
        maxElemIndex = freq_data.index(max(freq_data))
        peakFreq = self.freq[maxElemIndex]*1e3 # freq in Hz
        theta = U.WithUnit( np.arccos(peakFreq/(chi*bareRabi['Hz']))*180.0/np.pi , 'deg' )
        return theta

if __name__ == "__main__":

    bareRabi = U.WithUnit(56136.0, 'Hz')

    date = '2013Jul16'
    datasetname = '0054_02'
    #datasetname = '0056_00'
    f = Flopalyzer(date, datasetname)
    print "Projection: " + str(f.compute_projection(bareRabi))

    f.make_plots()
