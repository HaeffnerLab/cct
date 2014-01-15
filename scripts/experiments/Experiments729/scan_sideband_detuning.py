from common.abstractdevices.script_scanner.scan_methods import experiment
from excitation_729 import excitation_729
from cct.scripts.scriptLibrary.common_methods_729 import common_methods_729 as cm
from cct.scripts.scriptLibrary import dvParameters
import time
import labrad
from labrad.units import WithUnit
from numpy import linspace
from common.okfpgaservers.pulser.pulse_sequences.plot_sequence import SequencePlotter


class scan_sideband_detuning(experiment):
    
    name = 'ScanSBCoolingDetuning'
    trap_frequencies = [
                        ('TrapFrequencies','axial_frequency'),
                        ('TrapFrequencies','radial_frequency_1'),
                        ('TrapFrequencies','radial_frequency_2'),
                        ('TrapFrequencies','rf_drive_frequency'),                       
                        ]
    required_parameters = [
                           ('RabiFlopping','rabi_amplitude_729'),
                           ('RabiFlopping','manual_frequency_729'),
                           ('RabiFlopping','line_selection'),
                           ('RabiFlopping','rabi_amplitude_729'),
                           ('RabiFlopping','frequency_selection'),
                           ('RabiFlopping','sideband_selection'),
                           
                           ('RabiFlopping_Sit', 'sit_on_excitation'),
                           ('SidebandCoolingDetuningScan', 'manual_scan')
                           ]

    optional_parameters = [
        ('SidebandCoolingDetuningScan', 'manual_scan')
        ]
    required_parameters.extend(trap_frequencies)
    required_parameters.extend(excitation_729.required_parameters)
    #removing parameters we'll be overwriting, and they do not need to be loaded
    required_parameters.remove(('Excitation_729','rabi_excitation_amplitude'))
    required_parameters.remove(('Excitation_729','rabi_excitation_duration'))
    required_parameters.remove(('Excitation_729','rabi_excitation_frequency'))
    required_parameters.remove(('SidebandCooling', 'sideband_cooling_detuning_729'))

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
        self.pulser = self.cxn.pulser
        self.sb_det_save_context = cxn.context()
    
    def setup_sequence_parameters(self):
        self.load_frequency()
        self.parameters['Excitation_729.rabi_excitation_amplitude'] = self.parameters.RabiFlopping.rabi_amplitude_729
        self.parameters['Excitation_729.rabi_excitation_duration'] = self.parameters.RabiFlopping_Sit.sit_on_excitation
        minim,maxim,steps = self.parameters.SidebandCoolingDetuningScan.manual_scan
        minim = minim['kHz']; maxim = maxim['kHz']
        self.scan = linspace(minim, maxim, steps)
        self.scan = [WithUnit(pt, 'kHz') for pt in self.scan]
    
    def load_frequency(self):
        #reloads trap frequencyies and gets the latest information from the drift tracker
        self.reload_some_parameters(self.trap_frequencies)
        flop = self.parameters.RabiFlopping
        frequency = cm.frequency_from_line_selection(flop.frequency_selection, flop.manual_frequency_729, flop.line_selection, self.drift_tracker)
        trap = self.parameters.TrapFrequencies
        if flop.frequency_selection == 'auto':
            frequency = cm.add_sidebands(frequency, flop.sideband_selection, trap)
        self.parameters['Excitation_729.rabi_excitation_frequency'] = frequency

    def setup_data_vault(self):
        localtime = time.localtime()
        datasetNameAppend = time.strftime("%Y%b%d_%H%M_%S",localtime)
        dirappend = [ time.strftime("%Y%b%d",localtime) ,time.strftime("%H%M_%S", localtime)]
        directory = ['','Experiments']
        directory.extend([self.name])
        directory.extend(dirappend)
        self.dv.cd(directory ,True, context = self.sb_det_save_context)
        self.dv.new('Detuning Scan {}'.format(datasetNameAppend),[('detuning', 'kHz')],[('Excitation Probability','Arb','Arb')], context = self.sb_det_save_context)
        window_name = self.parameters.get('SidebandCoolingDetuningScan.window_name', ['Detuning Scan'])
        self.dv.add_parameter('Window', window_name, context = self.sb_det_save_context)
        self.dv.add_parameter('plotLive', True, context = self.sb_det_save_context)

    def run(self, cxn, context):
        self.setup_data_vault()
        self.setup_sequence_parameters()
        self.load_frequency()
        self.pulser.switch_auto('397mod')
        self.pulser.switch_auto('parametric_modulation')        
        self.setup_sequence_parameters()
        
        for i, det in enumerate(self.scan):
            should_stop = self.pause_or_stop()
            if should_stop: break
            self.parameters['SidebandCooling.sideband_cooling_detuning_729'] = det
            self.excite.set_parameters(self.parameters)
            excitation = self.excite.run(cxn, context)
            self.dv.add((det, excitation), context = self.sb_det_save_context)
            self.update_progress(i)
        # ttl = self.cxn.pulser.human_readable_ttl()
        # dds = self.cxn.pulser.human_readable_dds()
        # channels = self.cxn.pulser.get_channels().asarray
        # sp = SequencePlotter(ttl.asarray, dds.aslist, channels)
        # sp.makePlot()

    def finalize(self, cxn, context):
        self.save_parameters(self.dv, cxn, self.cxnlab, self.sb_det_save_context)

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
    exprt = scan_sideband_detuning(cxn = cxn)
    ident = scanner.register_external_launch(exprt.name)
    exprt.execute(ident)
