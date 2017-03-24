'''
Measure the temperature in one mode
'''

from common.abstractdevices.script_scanner.scan_methods import experiment
from spectrum import spectrum
from labrad.units import WithUnit
from treedict import TreeDict
import time
import numpy as np

class measure_temperature(experiment):

    name = 'MeasureModeTemperature'

    required_parameters = [
        ('Spectrum', 'temperature'), # sensitivity selection for heating rate scan

        ('Temperature', 'sideband_selection'),
        ('Temperature', 'autofit_spectrum'),
        ('Temperature', 'rabi_flop_rsb'),
        ]

    required_parameters.extend(spectrum.required_paremeters)

    #removing parameters we'll be overwriting, and they do not need to be loaded    
    remove_parameters = [
        ('Spectrum','custom'),
        ('Spectrum','normal'),
        ('Spectrum','fine'),
        ('Spectrum','ultimate'),
        ('Spectrum','opticalpumping'),
        ('Spectrum','carrier'),

        ('Spectrum','manual_amplitude_729'),
        ('Spectrum','manual_excitation_time'),
        ('Spectrum','manual_scan'),
        ('Spectrum','scan_selection'),
        ('Spectrum','sensitivity_selection'),
        ('Spectrum','sideband_selection')
        ]

    for p in remove_parameters:
        required_parameters.remove(p)

    optional_parameters = [('Temperature', 'bsb_scan_dataset'),
                           ('Temperature', 'rsb_scan_dataset'),
                           ('Temperature', 'bsb_flop_dataset'),
                           ('Temperature', 'rsb_flop_dataset'),
                           ('Temperature', 'bsb_scan_save_directory'),
                           ('Temperature', 'rsb_scan_save_directory'),
                           ('Temperature', 'bsb_flop_save_directory'),
                           ('Temperature', 'rsb_flop_save_directory')
                           ]

    def initialize(self, cxn, context, ident):

        self.cxnlab = labrad.connect('192.168.169.49')
        self.drift_tracker = cxn.sd_tracker
        self.dv = cxn.data_vault
        self.data_analyzer = cxn.data_analyzer
        self.pv = cxn.parameter_vault

        self.temperature_save_context = cxn.context()

        temp = self.paramters.Temperature

        # set the sideband selection in a format the drift tracker will accept
        pos = ['axial', 'radial', 'radial'].index(temp.sideband_selection)
        
        self.rsb_sel = [0]*4
        self.bsb_sel = [0]*4
        self.rsb_sel[pos] = -1
        self.bsb_sel[pos] = 1

        self.freqDict = {
            'axial': ('TrapFrequencies', 'axial_frequency'),
            'radial1': ('TrapFrequencies','radial_frequency_1'),
            'radial2': ('TrapFrequencies','radial_frequency_2')
            }

        self.spectrum = self.make_experiment(spectrum)
        self.spectrum.initialize(cxn, context, ident)

        self.make_dv_dirs() # override the default save locations

    def make_dv_dirs(self):
        localtime = time.localtime()
        dirappend = [ time.strftime("%Y%b%d",localtime) ,time.strftime("%H%M_%S", localtime)]
        dir = ['','Experiments']
        dir.extend([self.name])
        dir.extend(dirappend)

        datasetNameAppend = time.strftime("%Y%b%d_%H%M_%S",localtime)

        self.blue_scan_dir = self.parameters.get('Temperature.bsb_scan_save_directory', dir)
        self.red_scan_dir = self.parameters.get('Temperature.rsb_scan_save_directory', dir)
        self.blue_flop_dir = self.parameters.get('Temperature.bsb_flop_save_directory', dir)
        self.red_flop_dir = self.parameters.get('Temperature.rsb_flop_save_directory', dir)

        self.blue_scan_dataset = self.parameters.get('Temperature.bsb_scan_dataset' 'BSB spectrum {}'.format(datasetNameAppend))
        self.red_scan_dataset = self.parameters.get('Temperature.rsb_scan_dataset' 'RSB spectrum {}'.format(datasetNameAppend))
        self.blue_flop_dataset = self.parameters.get('Temperature.bsb_flop_dataset' 'BSB flop {}'.format(datasetNameAppend))
        self.red_flop_dataset = self.parameters.get('Temperature.rsb_flop_dataset' 'RSB flop {}'.format(datasetNameAppend))

    def update_sidebands(self, line):
        '''
        Update the trap frequency stored in the parameter vault
        '''
        
        sideband = line['center']
        sb_selection = self.parameters.Temperature.sideband_selection
        collection, name = self.freqDict[sb_selection]
        try:
            line = self.drift_tracker.get_current_line(line_selection)
            diff = abs( line - sideband )
            self.pv.set_parameter(collection, name, diff)
        except:
            raise Exception ("Unable to get {0} from drift tracker".format(line_slection))

    def update_pi_times(self, flop):

        pi_time = flop['pi_time']
        [span, resolution, duration, amplitude] = self.parameters.Spectrum['Temperature']
        duration = pi_time

        temperature_scan = [span, resolution, duration, amplitude)

        self.pv.set_parameter('Spectrum', 'Temperature', temperature_scan)


    def run(self, cxn, context):

        sp = self.parameters.Spectrum
        fl = self.parameters.RabiFlopping
        
        blue_spectrum_replace = TreeDict.fromdict({
                'Spectrum.sensitivity_selection': sp.temperature,
                'Spectrum.sideband_selection': self.bsb_sel,
                'Spectrum.save_dir': self.blue_scan_dir,
                'Spectrum.dataset': self.blue_scan_dataset,
                })

        red_spectrum_replace = TreeDict.fromdict({
                'Spectrum.sensitivity_selection': sp.temperature,
                'Spectrum.sideband_selection': self.rsb_sel,
                'Spectrum.save_dir': self.red_scan_dir,
                'Spectrum.dataset': self.red_scan_dataset
                })

        blue_flop_replace = TreeDict.fromdict({
                })

        red_flop_replace = TreeDict.fromdict({
                })

        # blue flop to get pi time
        self.rabi_flop.run(blue_flop_replace)
        flop = self.rabi_flop.get_fit()
        self.update_pi_times(flop)
        
        # blue frequency scan
        self.spectrum.run(blue_spectrum_replace)
        line = self.spectrum.get_fit()
        self.update_sidebands(line)
        
        # red frequency scan
        self.spectrum.run(red_spectrum_replace)
        line = self.spectrum.get_fit()
        self.update_sidebands(line)
        
        # rabi flop on the red sideband to complete the dataset
        self.rabi_flop.run(red_flop_replace)
