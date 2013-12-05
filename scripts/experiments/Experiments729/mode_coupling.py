'''
Pulse sequence is:

state preparation
Pi pulse on blue s.b.
Mode coupling for scanning time t
Analysis

'''

from common.abstractdevices.script_scanner.scan_methods import experiment
from excitation_mode_coupling import excitation_mode_coupling
from cct.scripts.scriptLibrary.common_methods_729 import common_methods_729 as cm
from cct.scripts.scriptLibrary import dvParameters
import time
import labrad
from labrad.units import WithUnit
from numpy import linspace
from common.okfpgaservers.pulser.pulse_sequences.plot_sequence import SequencePlotter

class mode_coupling(experiment):

    name = 'ModeCoupling'

    required_parameters = [
        ('ParametricCoupling', 'manual_scan'),
        ('RabiFlopping','rabi_amplitude_729'),
        ('RabiFlopping','manual_frequency_729'),
        ('RabiFlopping','line_selection'),
        ('RabiFlopping','rabi_amplitude_729'),
        ('RabiFlopping','frequency_selection'),
        ('RabiFlopping','sideband_selection'),
        
        ('RabiFlopping_Sit', 'sit_on_excitation'),
        ]
    required_parameters.extend(excitation_mode_coupling.required_parameters)

    optional_parameters = [
        ('ParametericCoupling', 'window_name')
        ]

    # we will calculate these later on
    required_parameters.remove(('Excitation_729','rabi_excitation_amplitude'))
    required_parameters.remove(('Excitation_729','rabi_excitation_duration'))
    required_parameters.remove(('Excitation_729','rabi_excitation_frequency'))
    required_parameters.remove(('PiPulse', 'rabi_amplitude_729'))
    required_parameters.remove(('PiPulse', 'rabi_excitation_frequency'))


    def initialize(self, cxn, context, ident):
        self.ident = ident
        self.excite = self.make_experiment(excitation_729)
        self.excite.initialize(cxn, context, ident)
        self.scan = []
        self.amplitude = None
        self.duration = None
        self.cxnlab = labrad.connect('192.168.169.49') #connection to labwide network
        self.drift_tracker = cxn.sd_tracker
        self.dv = cxn.data_vault
        self.mode_coupling_save_context = cxn.context()
        self.pulser = cxn.pulser

    def setup_sequence_parameters(self):
        coupling = self.parameters.ModeCoupling
        piPulse = self.parameters.PiPulse
        flop = self.parameters.RabiFlopping
        analysis_frequency = cm.frequency_from_line_selection(flop.frequency_selection, flop.manual_frequency_729, flop.line_selection, self.drift_tracker)
        pi_frequency = cm.frequency_from_line_selection(piPulse.frequency_selection, piPulse.manual_frequency_729, piPulse.line_selection, self.drift_tracker)
        trap = self.parameters.TrapFrequencies
        if flop.frequency_selection == 'auto':
            analysis_frequency = cm.add_sidebands(analysis_frequency, flop.sideband_selection, trap)
            pi_frequency = cm.add_sidebands(pi_frequency, piPulse.sideband_selection, trap)
        self.parameters['Excitation_729.rabi_excitation_frequency'] = analysis_frequency + flop.offset_frequency
        self.parameters['Excitation_729.rabi_excitation_amplitude'] = flop.rabi_amplitude_729
        self.parameters['PiPulse.rabi_excitation_frequency'] = pi_frequency
        minim,maxim,steps = coupling.manual_scan
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
        self.dv.cd(directory ,True, context = self.mode_coupling_save_context)
        self.dv.new('Parametric Coupling {}'.format(datasetNameAppend),[('Excitation', 'us')],[('Excitation Probability','Arb','Arb')], context = self.rabi_flop_save_context)
        window_name = self.parameters.get('ParametricCoupling.window_name', ['Parametric Coupling'])
        self.dv.add_parameter('Window', window_name, context = self.mode_coupling_save_context)
        self.dv.add_parameter('plotLive', True, context = self.mode_coupling_save_context)

    def run(self, cxn, context):
        self.setup_data_vault()
        self.setup_sequence_parameters()
        
        for i, duration in enumerate(self.scan):
            should_stop = self.pause_or_stop()
            if should_stop: break

            self.parameters['ParametricCoupling.parametric_coupling_duration'] = duration
            self.excite.set_parameters(self.parameters)
            excitation = self.excite.run(cxn, context)
            self.dv.add((duration, excitation), context = self.mode_coupling_save_context)
            self.update_progress(i)
            
        #dds = self.cxn.pulser.human_readable_dds()
        #ttl = self.cxn.pulser.human_readable_ttl()
        #channels = self.cxn.pulser.get_channels().asarray
        #sp = SequencePlotter(ttl.asarray, dds.aslist, channels)
        #sp.makePlot()

    def finalize(self, cxn, context):
        self.save_parameters(self.dv, cxn, self.cxnlab, self.rabi_flop_save_context)

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
    exprt = mode_coupling(cxn = cxn)
    ident = scanner.register_external_launch(exprt.name)
    exprt.execute(ident)
