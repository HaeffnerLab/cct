from common.abstractdevices.script_scannerscan_methods import experiment
from spectrum import spectrum
from labrad.units import WithUnit
from treedict import TreeDict

class heating_rate(experiment):

    name = 'HeatingRate'

    required_parameters = [
        ('Spectrum', 'heating_rate'), # sensitivity selection for heating rate scan

        ('HeatingRate', 'sideband_selection'),
        ('HeatingRate', 'autofit_spectrum'),
        ('HeatingRate', 'rabi_flop_rsb'),
        ]

    required_parameters.extend(spectrum.required_parameters)

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

    optional_parameters = []

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

        hr = self.parameters.HeatingRate
        if hr == 'axial':
            self.red_sb_sel = [-1, 0, 0, 0]
            self.blue_sb_sel = [1, 0, 0, 0]
        elif hr == 'radial1':
            self.red_sb_sel = [0, -1, 0, 0]
            self.blue_sb_sel = [0, 1, 0, 0]
        elif hr == 'radial2':
            self.red_sb_sel = [0, 0, -1, 0]
            self.blue_sb_sel = [0, 0, 1, 0]

        self.spectrum = self.make_experiment(spectrum)
        self.spectrum.initialize(cxn, context, ident)

        self.make_dv_dirs()

    def make_dv_dirs(self):
        self.localtime = time.localtime()
        self.baseDir = 'Experiments.HeatingRate.{}.{}'.format(time.strftime('%Y%b%d', localtime), time.strftime('%H%M_%S', localtime))

    def scan_sideband(self, sideband, cxn, context, ident):

        if sideband == 'blue_init':
            # scan to find the frequency
            hr = self.parameters.HeatingRate
            
            replace = TreeDict.fromdict({
                    'Spectrum.sensitivity_selection':'heating_rate',
                    'Spectrum.scan_selection':'auto',
                    'Spectrum.sideband_selection': self.blue_sb_sel,
                    'Spectrum.save_directory':
                    })

            self.spectrum.set_parameters(replace)
            
        elif sideband == 'blue':
            
