from common.abstractdevices.script_scannerscan_methods import experiment
from labrad.units import WithUnit
from treedict import TreeDict

class heating_rate(experiment):

    name = 'HeatingRate'

    required_parameters = [
        ('Spectrum', 'heating_rate'), # sensitivity selection for heating rate scan

        ('HeatingRate', 'sideband_selection'),
        ('HeatingRate', 'autofit_spectrum'),
        ('HeatingRate', 'rabi_flop_rsb'),

        ('TrapFrequencies','axial_frequency'),
        ('TrapFrequencies','radial_frequency_1'),
        ('TrapFrequencies','radial_frequency_2'),
        ('TrapFrequencies','rf_drive_frequency')

        ]

    required_parameters.extend(excitation_729.required_parameters)
    #removing parameters we'll be overwriting, and they do not need to be loaded
    required_parameters.remove(('Excitation_729','rabi_excitation_amplitude'))
    required_parameters.remove(('Excitation_729','rabi_excitation_duration'))
    required_parameters.remove(('Excitation_729','rabi_excitation_frequency'))

    optional_parameters = [ ]

    def initialize(self, cxn, context, ident):
        self.ident = ident

        self.excite = self.make_experiment(excitation_729)
        self.excite.initialize(cxn, context, ident)
        self.scan = []

        self.amplitude = None
        self.duration = None

        self.cxnlab = labrad.connect('192.168.169.49')
        self.drift_tracker = cxn.sd_tracker
        self.dv = cxn.data_vault
        self.data_analyzer = cxn.data_analyzer
        
        self.heating_rate_save_context = cxn.context()
        
        self.initialize_data_vault()
        
    def setup_sequence_flop(self):
        flop = self.parameters.RabiFlopping
        frequency = cm.frequency_from_line_selection(flop.frequency_selection, flop.manual_frequency_729, flop.line_selection, self.drift_tracker)
        frequency = cm.add_sidebands(frequency, flop.sideband_selection, trap)

    def correct_sideband(self, freq):
        trap = self.parameters.TrapFrequencies

    def initialize_data_vault(self):
        localtime = time.localtime()
        datasetNameAppend = time.strftime("%Y%b%d_%H%M_%S",localtime)
        dirappend = [ time.strftime("%Y%b%d",localtime) ,time.strftime("%H%M_%S", localtime)]
        directory = ['','Experiments']
        directory.extend([self.name])
        directory.extend(dirappend)
        base_dir = []
        base_dir.extend(directory)

        bsb_scan_dir = []
        rsb_scan_dir = []
        bsb_flop_dir = []
        rsb_flop_dir = []
        heating_rate_dir = []

        [x.extend(base_dir) for x in [bsb_scan_dir, rsb_scan_dir, bsb_flop_dir, rsb_flop_dir]]

        bsb_scan_dir.append('BSB_freq_scan')
        rsb_scan_dir.append('RSB_freq_scan')
        bsb_flop_dir.append('BSB_excitation_scan')
        rsb_flop_dir.append('RSB_excitation_scan')

        self.dv_parameter_dict = {
            'bsb_scan': (bsb_scan_dir, 'Blue freq scan -- ', [('Freq', 'MHz')],[('Excitation Probability','Arb','Arb')], 'Blue SB Scan'),
            'rsb_scan': (rsb_scan_dir, 'Red freq scan -- ', [('Freq', 'MHz')],[('Excitation Probability','Arb','Arb')], 'Red SB Scan'),
            'bsb_flop': (bsb_flop_dir, 'Blue excitation scan -- ', [('Excitation', 'us')],[('Excitation Probability','Arb','Arb')], 'Blue SB Flop'),
            'rsb_flop': (rsb_flop_dir, 'Red excitation scan -- ', [('Excitation', 'us')],[('Excitation Probability','Arb','Arb')], 'Red SB Flop'),
            'bsb_init_scan': (base_dir, 'Blue initial scan -- ', [('Freq', 'MHz')],[('Excitation Probability','Arb','Arb')], 'Blue SB Scan')
            }
        
    def setup_data_vault(self, type, heating_time = None):
        
        try:
            dir, dataset, dv1, dv2, window_name = self.dv_parameter_dict[type]
        except:
            print "Incorrect type specified"

        if heating_time is not None: dataset += str(heating_time)
        self.dv.cd(dir, True, context = self.heating_rate_save_context)x
        self.dv.new(dataset, dv1, dv2, context = self.heating_rate_save_context)
        self.dv.add_parameter('Window', window_name, context = self.heating_rate_save_context)
        self.dv.add_parameter('plotLive', True, context = self.heating_rate_save_context)
        return dir, dataset
    
    def scan_sideband(self, sb, heating_time, cxn, context):
        if sb == "blue_init":
            scan = self.blue_scan
            dir, dataset = self.setup_data_vault('bsb_init_scan')
        if sb == "blue":
            scan = self.blue_scan
            dir, dataset = self.setup_data_vault('bsb_scan', heating_time)
        if sb == "red":
            scan = self.red_scan
            dir, dataset = self.setup_data_vault('rsb_scan', heating_time)
        for freq in scan:
            should_stop = self.pause_or_stop()
            if should_stop: break
            self.parameters['Excitation_729.rabi_excitation_frequency'] = freq
            self.excite_spectrum.set_parameters(self.parameters)
            excitation = self.excite_spectrum.run(cxn, context)
            self.dv.add((freq, excitation), context = heating_rate_save_context)

        if self.parameters['HeatingRate.autofit_spectrum']:
            '''
            Fit the sideband, and put the frequency back in
            '''
            key = self.data_analyzer.load_data(dir, dataset)
            self.data_analyzer.set_parameter(key, 'FWHM', 0., True, is_auto = True)
            self.data_analyzer.set_parameter(key, 'center', 0.0, True, is_auto = True)
            self.data_analyzer.set_parameter(key, 'height', 1.0, True, is_auto = True)
            self.data_analyzer.set_parameter(key, 'bgrnd', 0.0, False, is_auto = True)

            self.data_analyzer.fit(key)

            center = self.data_analyzer.get_parameter(key, 'center')
            height = self.data_analyzer.get_parameter(key, 'height')
            self.data_analyzer.delete_workspace(key)

            return height

    def flop_sideband(self, sb, heating_time, cxn, context):
        pass

    def run(self, cxn, context):
        # first find the blue sideband at the interrogation power to find the frequency
        self.scan_sideband('blue_init', None, cxn, context)

        for i, ti in enumerate(self.heating_times):
            should_stop = self.pause_or_stop()
            if should_stop: break
            self.excitation_scan('blue', cxn, context)
            self.scan_sideband('blue', cxn, context)
            self.scan_sideband('red', cxn, context)
            self.excitation_scan('red', cxn, context)
            self.update_progress(i)
