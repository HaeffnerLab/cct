import sys;
sys.path.append('/home/cct/LabRAD/cct/scripts')
sys.path.append('/home/cct/LabRAD/cct/scripts/PulseSequences')
import numpy as np
from PulseSequences.TimeResolvedRecord import TimeResolved
from processFFT import processFFT
import datetime
import time as TIME
from scripts.experiments.SemaphoreExperiment import SemaphoreExperiment
from scripts.PulseSequences.TimeResolvedRecord import sample_parameters

class simpleFFT(SemaphoreExperiment):
    ''' Experiment for a simple FFT measurement '''
    def __init__(self):
        self.experimentPath = ['FFT','simpleFFT']
        self.processor = processFFT()
        self.experimentLabel = 'simpleFFT'

    def run(self):
        self.initialize()
        try:
            self.sequence()
        except Exception,e:
            print 'Had to stop with error:',e
        finally:
            self.finalize()

    def initialize(self):
        print 'Started: {}'.format(self.experimentPath)
        self.percentDone = 0.0
        self.import_labrad()
        #self.setup_data_vault()
        self.sequence_parameters = self.setup_sequence_parameters()
        self.setup_pulser()

    def import_labrad(self):
        import labrad
        self.cxn = cxn = labrad.connect()
        self.cxnlab = labrad.connect('192.168.169.49') #connection to labwide network
        self.dv = self.cxn.data_vault
        self.readout_save_context = self.cxn.context()
        self.histogram_save_context = self.cxn.context()
        self.pulser = self.cxn.pulser
        self.sem = cxn.semaphore
        self.dv = cxn.data_vault
        self.p = self.populate_parameters(self.sem, self.experimentPath)
    
    def setup_sequence_parameters(self):
        sequence_parameters = {}.fromkeys(sample_parameters.parameters)
        check = self.check_parameter
        common_values = dict([(key,check(value)) for key,value in self.p.iteritems() if key in sequence_parameters])
        sequence_parameters.update(common_values)
        sequence_parameters['centerFreq'] = self.check_parameter(self.p.centerFreq)
        sequence_parameters['recordTime'] = self.check_parameter(self.p.recordTime)
        sequence_parameters['freqOffset'] = self.check_parameter(self.p.freqOffset)
        sequence_parameters['freqSpan'] = self.check_parameter(self.p.freqSpan)
        sequence_parameters['numToAverage'] = self.check_parameter(self.p.numToAverage)
        return sequence_parameters
    
    def setup_pulser(self):
        params = {
                  'recordTime': self.sequence_parameters['recordTime']
                  }
        print params
        seq = TimeResolved(self.pulser)
        self.pulser.new_sequence()
        seq.setVariables(**params)
        seq.defineSequence()
        self.pulser.program_sequence()
    
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
        
    def sequence(self):
        pwr = np.zeros_like(self.freqs)
        numToAverage = self.check_parameters(self.p.numToAverage)
        for i in range(numToAverage):
            self.percentDone = 100.0 * i/numToAverage
            self.pulser.reset_timetags()
            self.pulser.start_single()
            self.pulser.wait_sequence_done()
            self.pulser.stop_sequence()
            timetags = self.pulser.get_timetags().asarray
            print 'photons counted', timetags.size
            pwr += self.processor.getPowerSpectrum(self.freqs, timetags, self.recordTime, self.timeRes)
        pwr = pwr / float(self.numToAverage)
        self.saveData(pwr)
        self.pwr = pwr
        self.peakArea = self.getPeakArea(3)
        self.percentDone = 100.0
        
    def saveData(self, pwr):
        now = datetime.datetime.now()
        date = now.strftime("%Y%m%d")
        self.dv.cd(['',date,'FFT'],True)
        name = self.dv.new('FFT',[('Freq', 'Hz')], [('Power','Arb','Arb')] )
        data = np.array(np.vstack((self.freqs,pwr)).transpose(), dtype = 'float')
        self.dv.add_parameter('plotLive',True)
        self.dv.add(data)
        print 'Saved {}'.format(name)

    def finalize(self):
        self.sem.finish_experiment(self.experimentPath, self.percentDone)
        self.cxn.disconnect()
        self.cxnlab.disconnect()
        print 'Finished: {0}, {1}'.format(self.experimentPath, self.dirappend)

if  __name__ == '__main__':
    #freqOffset = -1375 #Hz, the offset between the counter clock and the rf synthesizer clock
    exprt = simpleFFT()
    exprt.run()
