from common.abstractdevices.script_scanner.scan_methods import experiment
from excitations import excitation_ramsey
from cct.scripts.scriptLibrary.common_methods_729 import common_methods_729 as cm
from cct.scripts.scriptLibrary import dvParameters
import time
import labrad
from labrad.units import WithUnit
from numpy import linspace
import numpy as np
from scipy import optimize

def squared_loss(params, y):
    C, phi, b = params
    x = np.array([0., 90., 180., 270.])
    e = y*(1-y)/np.sqrt(100.)
    dy = y - ((C/2)*(1 + np.sin(np.pi*x/180. + phi)) + b)
    return np.sum(0.5 * (dy / e) ** 2)

class ramsey_scangap_contrast(experiment):
    
    name = 'RamseyScanGapContrast'
    ramsey_required_parameters = [
                           ('RamseyScanGap', 'detuning'),
                           ('RamseyScanGap', 'scangap'),
                           
                           ('RabiFlopping','rabi_amplitude_729'),
                           ('RabiFlopping','manual_frequency_729'),
                           ('RabiFlopping','line_selection'),
                           ('RabiFlopping','rabi_amplitude_729'),
                           ('RabiFlopping','frequency_selection'),
                           ('RabiFlopping','sideband_selection'),
                           
                           ('TrapFrequencies','axial_frequency'),
                           ('TrapFrequencies','radial_frequency_1'),
                           ('TrapFrequencies','radial_frequency_2'),
                           ('TrapFrequencies','rf_drive_frequency'),
                           ]
    
    @classmethod
    def all_required_parameters(cls):
        parameters = set(cls.ramsey_required_parameters)
        parameters = parameters.union(set(excitation_ramsey.all_required_parameters()))
        parameters = list(parameters)
        #removing parameters we'll be overwriting, and they do not need to be loaded
        parameters.remove(('Excitation_729','rabi_excitation_amplitude'))
        parameters.remove(('Excitation_729','rabi_excitation_frequency'))
        parameters.remove(('Ramsey','ramsey_time'))
        return parameters
    
    def initialize(self, cxn, context, ident):
        self.ident = ident
        self.excite = self.make_experiment(excitation_ramsey)
        self.excite.initialize(cxn, context, ident)
        self.scan = []
        self.amplitude = None
        self.duration = None
        self.cxnlab = labrad.connect('192.168.169.49') #connection to labwide network
        self.drift_tracker = cxn.sd_tracker
        self.dv = cxn.data_vault
        self.data_save_context = cxn.context()
        self.contrast_save_context = cxn.context()
        self.setup_data_vault()
    
    def setup_sequence_parameters(self):
        flop = self.parameters.RabiFlopping
        frequency = cm.frequency_from_line_selection(flop.frequency_selection, flop.manual_frequency_729, flop.line_selection, self.drift_tracker)
        trap = self.parameters.TrapFrequencies
        if flop.frequency_selection == 'auto':
            frequency = cm.add_sidebands(frequency, flop.sideband_selection, trap)   
        frequency += self.parameters.RamseyScanGap.detuning
        #print frequency
        self.parameters['Excitation_729.rabi_excitation_frequency'] = frequency
        self.parameters['Excitation_729.rabi_excitation_amplitude'] = flop.rabi_amplitude_729
        minim,maxim,steps = self.parameters.RamseyScanGap.scangap
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
        #dependants = [('Excitation','Ion {}'.format(ion),'Probability') for ion in range(output_size)]
        dependents = [('Excitation', 'Phase 0', 'Probability'), ('Excitation', 'Phase 90', 'Probability'), ('Excitation', 'Phase 180', 'Probability'), ('Excitation', 'Phase 270', 'Probability')]
        self.dv.cd(directory, True,context = self.data_save_context)
        self.dv.cd(directory, True,context = self.contrast_save_context)
        self.dv.new('{0} {1} Parity Contrast'.format(self.name, datasetNameAppend),[('Excitation', 'us')], [('Contrast','Contrast','Probability')] , context = self.contrast_save_context)        
        self.dv.new('{0} {1}'.format(self.name, datasetNameAppend),[('Excitation', 'us')], dependents , context = self.data_save_context)
        window_name = self.parameters.get('RamseyScanGap.window_name', ['Ramsey Gap Scan'])
        self.dv.add_parameter('Window', window_name, context = self.data_save_context)
        self.dv.add_parameter('plotLive', True, context = self.data_save_context)
        self.dv.add_parameter('Window', window_name, context = self.contrast_save_context)
        self.dv.add_parameter('plotLive', True, context = self.contrast_save_context)        
    def run(self, cxn, context):
        self.setup_sequence_parameters()
        for i,duration in enumerate(self.scan):
            should_stop = self.pause_or_stop()
            if should_stop: break
            self.parameters['Ramsey.ramsey_time'] = duration

            phases = [WithUnit(x, 'deg') for x in [0., 90., 180., 270.]]
            p = []
            for phi in phases:
                self.parameters['Ramsey.second_pulse_phase'] = phi
                self.excite.set_parameters(self.parameters)
                excitation,readouts = self.excite.run(cxn, context, image_save_context = self.data_save_context)
                p.append(excitation[0])

            #c = 2*np.sqrt((p0 - 0.5*(p0 + p180))**2 + (p90 - 0.5*(p0 + p180) )**2)
            c, phase_shift, b = optimize.fmin(squared_loss, [0,0,0], args=[np.array(p)] ) # MaxLike optimization for contrast
            submission = [duration['us']]
            submission.extend(p)
            self.dv.add(submission, context = self.data_save_context)
            self.dv.add([duration['us'], np.abs(c)], context = self.contrast_save_context)
            self.update_progress(i)
     
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
    exprt = ramsey_scangap_contrast(cxn = cxn)
    ident = scanner.register_external_launch(exprt.name)
    exprt.execute(ident)