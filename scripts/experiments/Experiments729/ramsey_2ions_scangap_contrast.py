from common.abstractdevices.script_scanner.scan_methods import experiment
from excitations import excitation_ramsey_2ions
from cct.scripts.scriptLibrary.common_methods_729 import common_methods_729 as cm
from cct.scripts.scriptLibrary import dvParameters
import time
import labrad
from labrad.units import WithUnit
from numpy import linspace
import numpy as np

class ramsey_2ions_scangap_parity(experiment):
    
    name = 'Ramsey2ions_ScanGapContrast'
    ramsey2ions_required_parameters = [
                           ('Ramsey2ions_ScanGapParity', 'scangap'),
                           ('Ramsey2ions_ScanGapParity', 'first_ion_number'),
                           ('Ramsey2ions_ScanGapParity', 'second_ion_number'),
                           ('Ramsey2ions_ScanGapParity', 'line_selection'),
                           ('Ramsey2ions_ScanGapParity','sideband_selection'),
                           ('StateReadout', 'parity_threshold_high'),
                           ('StateReadout', 'parity_threshold_low'),
                            ('TrapFrequencies','axial_frequency'),
                            ('TrapFrequencies','radial_frequency_1'),
                            ('TrapFrequencies','radial_frequency_2'),
                            ('TrapFrequencies','rf_drive_frequency'),      
                           ]

    @classmethod
    def all_required_parameters(cls):
        parameters = set(cls.ramsey2ions_required_parameters)
        parameters = parameters.union(set(excitation_ramsey_2ions.all_required_parameters()))
        parameters = list(parameters)
        #removing parameters we'll be overwriting, and they do not need to be loaded
        parameters.remove(('Ramsey_2ions','excitation_frequency'))
        parameters.remove(('Ramsey_2ions','ramsey_time'))
        parameters.remove(('Ramsey_2ions','single_pass_phase'))
        return parameters
    
    def initialize(self, cxn, context, ident):
        self.ident = ident
        self.excite = self.make_experiment(excitation_ramsey_2ions)
        self.excite.initialize(cxn, context, ident)
        self.scan = []
        self.amplitude = None
        self.duration = None
        self.cxnlab = labrad.connect('192.168.169.49') #connection to labwide network
        self.drift_tracker = cxn.sd_tracker
        self.dv = cxn.data_vault
        self.data_save_context = cxn.context()
        self.contrast_save_context = cxn.context()
        self.parity_save_context = cxn.context()
        self.setup_data_vault()
    
    def setup_sequence_parameters(self):
        flop = self.parameters.Ramsey2ions_ScanGapParity
        trap = self.parameters.TrapFrequencies
        print "sideband_selection"
        print flop.sideband_selection
        excitation_frequency = cm.frequency_from_line_selection('auto', WithUnit(0.00, 'MHz'), flop.line_selection, self.drift_tracker)
        excitation_frequency = cm.add_sidebands(excitation_frequency, flop.sideband_selection, trap)
        print excitation_frequency
        self.parameters['Ramsey_2ions.excitation_frequency'] = excitation_frequency
        minim,maxim,steps = self.parameters.Ramsey2ions_ScanGapParity.scangap
        minim = minim['us']; maxim = maxim['us']
        self.scan = linspace(minim,maxim, steps)
        self.scan = [WithUnit(pt, 'us') for pt in self.scan]
        
    def setup_data_vault(self):
        localtime = time.localtime()
        datasetNameAppend = time.strftime("%Y%b%d_%H%M_%S",localtime)
        dirappend = [ time.strftime("%Y%b%d",localtime) ,time.strftime("%H%M_%S", localtime)]
        directory = ['','Experiments']
        directory.extend([self.name])
        directory.extend(dirappend)
        output_size = self.excite.output_size
        dependants = [('Excitation','Ion {}'.format(ion),'Probability') for ion in range(output_size)]
        self.dv.cd(directory, True,context = self.data_save_context)
        self.dv.cd(directory, True,context = self.contrast_save_context)
        self.dv.cd(directory, True, context = self.parity_save_context)
        self.dv.new('{0} {1}'.format(self.name, datasetNameAppend),[('Excitation', 'us')], dependants , context = self.data_save_context)
        self.dv.new('{0} {1} Parity Contrast'.format(self.name, datasetNameAppend),[('Excitation', 'us')], [('Contrast','Contrast','Probability')] , context = self.contrast_save_context)        
        self.dv.new('{0} {1} Parities'.format(self.name, datasetNameAppend), [('Excitation', 'us')], [('Parity', 'p0','Probability'),('Parity', 'p90','Probability'), ('Parity', 'p180','Probability')], context = self.parity_save_context)

        window_name = self.parameters.get('RamseyScanGap.window_name', ['Ramsey Gap Scan'])
        self.dv.add_parameter('Window', window_name, context = self.data_save_context)
        self.dv.add_parameter('plotLive', True, context = self.data_save_context)
        self.dv.add_parameter('Window', window_name, context = self.contrast_save_context)
        self.dv.add_parameter('plotLive', True, context = self.contrast_save_context)
        self.dv.add_parameter('Window', window_name, context = self.parity_save_context)
        self.dv.add_parameter('plotLive', True, context = self.parity_save_context)
        
    def run(self, cxn, context):
        self.setup_sequence_parameters()
        threshold_low = self.parameters.StateReadout.parity_threshold_low
        threshold_high = self.parameters.StateReadout.parity_threshold_high
        position1 = int(self.parameters.Ramsey2ions_ScanGapParity.first_ion_number)
        position2 = int(self.parameters.Ramsey2ions_ScanGapParity.second_ion_number)
        for i,duration in enumerate(self.scan):
            should_stop = self.pause_or_stop()
            if should_stop: break
            self.parameters['Ramsey_2ions.ramsey_time'] = duration
            
            phi = WithUnit(0., 'deg')
            self.parameters['Ramsey.second_pulse_phase'] = phi
            self.excite.set_parameters(self.parameters)
            excitation,readouts = self.excite.run(cxn, context, image_save_context = self.data_save_context)
            p0 = excitation

            phi = WithUnit(90., 'deg')
            self.parameters['Ramsey.second_pulse_phase'] = phi
            self.excite.set_parameters(self.parameters)
            excitation,readouts = self.excite.run(cxn, context, image_save_context = self.data_save_context)
            p90 = excitation

            phi = WithUnit(180., 'deg')
            self.parameters['Ramsey.second_pulse_phase'] = phi
            self.excite.set_parameters(self.parameters)
            excitation,readouts = self.excite.run(cxn, context, image_save_context = self.data_save_context)
            p180 = excitation

            c = np.sqrt((p0 - 0.5*(p0 + p180))**2 + (p90 - 0.5*(p0 + p180) )**2)


            #parity = self.compute_parity_pmt(readouts, threshold_low, threshold_high)
            submission = [duration['us']]
            submission.extend(excitation)
            self.dv.add(submission, context = self.data_save_context)
            self.dv.add([duration['us'], c], context = self.contrast_save_context)
            self.dv.add([duration['us'], p0, p90, p180], context = self.parity_save_context)
            #self.excite.plot_current_sequence(cxn)
            self.update_progress(i)
    
    def compute_parity(self, readouts,pos1,pos2):
        '''
        computes the parity of the provided readouts
        '''
        #print readouts
        correlated_readout = readouts[:,pos1]+readouts[:,pos2]
        parity = (correlated_readout % 2 == 0).mean() - (correlated_readout % 2 == 1).mean()
        return parity

    def compute_parity_pmt(self, readouts,threshold_low,threshold_high):
        '''
        computes the parity of the provided readouts using a pmt
        '''
        even_parity = np.count_nonzero((readouts <= threshold_low)|(readouts >= threshold_high))
        print "even = ", even_parity
        odd_parity = np.count_nonzero((readouts >= threshold_low)&(readouts <= threshold_high))
        print "odd = ", odd_parity
        parity = (even_parity - odd_parity)/float(len(readouts))
        return parity
     
    def finalize(self, cxn, context):
        self.save_parameters(self.dv, cxn, self.cxnlab, self.data_save_context)

    def update_progress(self, iteration):
        progress = self.min_progress + (self.max_progress - self.min_progress) * float(iteration + 1.0) / len(self.scan)
        self.sc.script_set_progress(self.ident,  progress)

    def save_parameters(self, dv, cxn, cxnlab, context):
        measuredDict = dvParameters.measureParameters(cxn, cxnlab)
        dvParameters.saveParameters(dv, measuredDict, context)
        dvParameters.saveParameters(dv, dict(self.parameters), context)   

if __name__ == '__main__':
    cxn = labrad.connect()
    scanner = cxn.scriptscanner
    exprt = ramsey_2ions_scangap_parity(cxn = cxn)
    ident = scanner.register_external_launch(exprt.name)
    exprt.execute(ident)
