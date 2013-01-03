from cct.scripts.exeriments.SemaphoreExperiment import SemaphoreExperiment
from cct.scripts.scriptLibrary import dvParameters
import time
import datetime
import numpy

class Tickle(SemaphoreExperiment):

    def __init__(self):
        self.experimentPath = ['Compensation', 'Tickle']

    def run(self):
        self.initialize()
        try:
            self.sequence()
        except Exception,e:
            #print 'Had to stop sequence with error:', e

finally:
    self.finalize()

    def initialize(self):
        print 'Started: {}'.format(self.experimentPath)
        self.percentDone = 0.0
        self.import_labrad()
        self.setup_data_vault()        
        self.multipole_settings = self.dacserver.get_multipole_values()

    def import_labrad(self):
        import labrad
        self.cxn = cxn = labrad.connect()
        self.cxn2 = labrad.connect('192.168.169.30') # for the RS control
        self.dv = self.cxn.data_vault
        
        self.dacserver = self.cxn.cctdac_pulser
        self.rs = self.cxn2.rohdeschwarz_server
        self.rs.select_device('GPIB Bus - USB0::0x0AAD::0x0054::104543')
        self.reg = self.cxn.registry
        self.sem = cxn.semaphore
        self.p = self.populate_parameters(self.sem, self.experimentPath)

    def setup_data_vault(self):
        localtime = time.localtime()
        now = datetime.datetime.now()
        date = now.strftime("%Y-%m-%d")
        axis = self.check_parameters(self.p.compensation_axis)
        self.dirappend = [axis, time.strftime("%H%M_%S", localtime)]
        directory = ['',date]
        directory.extend(self.experimentPath)
        directory.extend(self.dirappend)
        self.dv.cd(directory, True )

        self.dv.add_parameter('Window', self.p.window_name)
        self.dv.add_parameter('plotLive',True)

    def setup_sequence_parameters(self):
        sequence_parameters = {}.fromkeys(sample_parameters.parameters)
        check = self.check_parameter
        common_values = dict([(key,check(value)) for key,value in self.p.iteritems() if key in sequence_parameters])
        sequence_parameters.update(common_values)
        sequence_parameters['frequency_397'] = check(self.p.frequency_397)
        return sequence_parameters

    
    def sequence(self):
        import labrad.types as T

        frequency_scan = self.check_paremeters(self.p.frequencies)
        compensation_scan = self.check_parameters(self.p.compensation_values)
        excitation_ampl = None
        duration = None
        reverse = False
        compensation_axis = self.check_parameters(self.p.compensation_axis)
        num_averages = self.check_parameters(self.p.num_averages)
        D = {}
        for v in self.multipole_values:
            D[v[0]] = v[1]
        
        initA = D[compensation_axis]
        del D[compensation_axis]

        for index1, comp in enumerate(compensation_scan):
            for index2, freq in enumerate(frequency_scan):
                self.percentDone = 100.0 * index1/ len(compensation_scan)

                if not should_continue:
                    print 'Not continuing'
                    return
                
                else:
                    # Here the magic happens                   
                    self.dacserver.set_multipole_values([(v, D[v]) for v in D.keys()] + [(axis, comp)])
                    graphName = compensation_axis + ': ' + str(comp)
                    name = self.dv.new(graphName,[('Frequency', 'Hz')], [('PMT Counts', 'PMT counts', 'PMT counts')])
                    self.dv.add_parameter(compensation_axis, comp)
                    self.dv.add_parameter('plotLive', True)

                    self.rs.frequency(self.T.Value(freq, 'MHz'))
                    self.rs.amplitude(self.T.Value(excitation_ampl, 'dBm'))
                    self.rs.onoff(True)
                    
                    pmtcount = self.pmt.get_next_counts('ON', num_averages, True)
                    self.dv.add(freq, pmtcount)
                    self.rsonff(False)

    def finalize(self):
        self.rsonoff(False)
        self.sem.finish_experiment(self.experimentPath, self.percentDone)
        D = {}
        for v in self.multipole_values:
            D[v[0]] = v[1]
        self.dacserver.set_multipole_values([(v, D[v]) for v in D.keys()]) # Go back to the original compensation setting
        self.cxn.disconnect()
        self.cxn2.disconnect()
