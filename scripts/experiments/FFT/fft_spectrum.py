import labrad
import numpy as np
from common.abstractdevices.script_scanner.scan_methods import experiment
from space_time.scripts.PulseSequences.subsequences.RecordTimeTags import record_timetags
from processFFT import processFFT
from treedict import TreeDict
import time
from space_time.scripts.scriptLibrary import dvParameters
from labrad.units import WithUnit

class fft_spectrum(experiment):
    
    name = 'FFT Spectrum'
    required_parameters = [
                           ('TrapFrequencies','rf_drive_frequency'),
                           ('FFT','average'),
                           ('FFT','frequency_offset'),
                           ('FFT','frequency_span'),
                           ('FFT','record_time'),
                           ]
    
    @classmethod
    def all_required_parameters(cls):
        parameters = set(cls.required_parameters)
        parameters = list(parameters)
        return parameters
    
    def initialize(self, cxn, context, ident):
        self.ident = ident
        self.processor = processFFT()
        self.average = int(self.parameters.FFT.average)
        self.record_time = self.parameters.FFT.record_time
        self.freq_span = self.parameters.FFT.frequency_span
        self.freq_offset = self.parameters.FFT.frequency_offset
        self.dv = cxn.data_vault
        self.pulser = cxn.pulser
        self.cxnlab = labrad.connect('192.168.169.49', password='lab', tls_mode='off') 
        self.fft_save_context = cxn.context()
        center_freq = self.parameters.TrapFrequencies.rf_drive_frequency
        self.time_resolution = self.pulser.get_timetag_resolution()
        self.freqs = self.processor.computeFreqDomain(self.record_time['s'], self.freq_span['Hz'],  self.freq_offset['Hz'], center_freq['Hz'])
        self.scan = [WithUnit(pt, 'Hz') for pt in self.freqs]
        self.programPulseSequence(self.record_time)
        try:
            self.grapher = cxn.grapher
        except: self.grapher = None
    
    def programPulseSequence(self, record_time):
        seq = record_timetags(TreeDict.fromdict({'RecordTimetags.record_timetags_duration': record_time}))
        seq.programSequence(self.pulser)
    
    def getTotalPower(self):
        '''computers the total power in the spectrum of the given frequencies'''
        spectrum = self.getPowerSpectrum()
        totalPower = self.processor.totalPower(spectrum)
        print 'Total Power {}'.format(totalPower)
        return totalPower
    
    def getPeakArea(self, ptsAround):
        '''Finds the maximum of the power spectrum, computers the area of the peak using ptsAround, then subtracts the background'''
        spectrum = self.getPowerSpectrum()
        peakArea = self.processor.peakArea(spectrum, ptsAround)
        print 'Peak Area {}'.format(peakArea)
        return peakArea

    def run(self, cxn, context):
        self.setup_data_vault()
        pwr = self.getPowerSpectrum()
        submission = zip(self.freqs,pwr)
        self.dv.add(submission, context = self.fft_save_context)
    
    def getPowerSpectrum(self):
        pwr = np.zeros_like(self.freqs)
        for i in range(self.average):
            should_stop = self.pause_or_stop()
            if should_stop: break
            self.pulser.reset_timetags()
            self.pulser.start_single()
            self.pulser.wait_sequence_done()
            self.pulser.stop_sequence()
            timetags = self.pulser.get_timetags()
            print timetags
            pwr += self.processor.getPowerSpectrum(self.freqs, timetags, self.record_time['s'], self.time_resolution)
            progress = self.min_progress + (self.max_progress - self.min_progress) * (i + 1) / float(self.average)
            self.sc.script_set_progress(self.ident,  progress)
        pwr = pwr / float(self.average)
        return pwr
    
    def setup_data_vault(self):
        localtime = time.localtime()
        datasetNameAppend = time.strftime("%Y%b%d_%H%M_%S",localtime)
        dirappend = [ time.strftime("%Y%b%d",localtime) ,time.strftime("%H%M_%S", localtime)]
        directory = ['','Experiments']
        directory.extend([self.name])
        directory.extend(dirappend)
        self.dv.cd(directory ,True, context = self.fft_save_context)
        dependants = [('Power','fft power spectrum','Arb. Units')]
        ds = self.dv.new('FFT {}'.format(datasetNameAppend),[('Power', 'Hz')], dependants , context = self.fft_save_context)
        window_name = self.parameters.get('FFT.window_name', ['fft'])[0]
        #window_name = self.get_window_name()
        self.dv.add_parameter('Window', [window_name], context = self.fft_save_context)
        #self.dv.add_parameter('plotLive', False, context = self.spectrum_save_context)
        self.save_parameters(self.dv, self.cxn, self.cxnlab, self.fft_save_context)
        sc = self.scan
        if self.grapher is not None:
            self.grapher.plot_with_axis(ds, window_name, sc, False)
            
    def save_parameters(self, dv, cxn, cxnlab, context):
        measuredDict = dvParameters.measureParameters(cxn, cxnlab)
        dvParameters.saveParameters(dv, measuredDict, context)
        dvParameters.saveParameters(dv, dict(self.parameters), context)
        cxnlab.disconnect()

#    def saveData(self, pwr):
#        self.dv.cd(['','QuickMeasurements','FFT'],True)
#        name = self.dv.new('FFT',[('Freq', 'Hz')], [('Power','Arb','Arb')] )
#        data = np.array(np.vstack((self.freqs,pwr)).transpose(), dtype = 'float')
#        self.dv.add_parameter('plotLive',True)
#        self.dv.add(data)
#        print 'Saved {}'.format(name)
    
    def finalize(self, cxn, context):
        pass

if __name__ == '__main__':
    #normal way to launch
    cxn = labrad.connect()
    scanner = cxn.scriptscanner
    exprt = fft_spectrum(cxn = cxn)
    ident = scanner.register_external_launch(exprt.name)
    exprt.execute(ident)
