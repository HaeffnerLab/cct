from common.abstractdevices.script_scanner.scan_methods import experiment
from spectrum import spectrum
from rabi_flopping import rabi_flopping
from labrad.units import WithUnit
from treedict import TreeDict
import time
import labrad

'''
General experiment to measure the temperature of a mode
'''


class temperature(experiment):

    name = 'Temperature'

    required_parameters = [ 
        ('Spectrum', 'temperature'), # sensitivity selection for heating rate scan
        
        ('Temperature', 'mode'),
        #('Temperature', 'autofit_spectrum'),
        #('Temperature', 'rabi_flop_rsb'),
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
        ('Spectrum','sideband_selection')]


    for p in remove_parameters:
        required_parameters.remove(p)

    optional_parameters = [
        ('Temperature', 'dataset'),
        ('Temperature', 'save_directory')
        ]

    def initialize(self, cxn, context, ident):
        
        self.ident = ident

        self.cxnlab = labrad.connect('192.168.169.49')
        self.drift_tracker = cxn.sd_tracker
        self.dv = cxn.data_vault
        self.pv = cxn.parametervault

        self.mode = self.parameters.Temperature.mode
        
        # write the red and blue sideband scan selections in a form that the drift
        # tracker will recognize
        self.rsb_sel = [0, 0, 0, 0]
        self.bsb_sel = [0, 0, 0, 0]
        j = ['radial_frequency_1', 'radial_frequency_2', 'axial_frequency'].index(self.mode)
        self.rsb_sel[j] = -1
        self.bsb_sel[j] = 1

        self.spectrum = self.make_experiment(spectrum)
        self.flop = self.make_experiment(rabi_flopping)
        self.spectrum.initialize(cxn, context, ident)
        self.temp_save_context = cxn.context()
        self.flop.initialize(cxn, context, ident)
        self.setup_data_vault_dirs()

    def setup_data_vault_dirs(self):
        localtime = time.localtime()
        try:
            dir = self.parameters.get('Temperature.save_directory')
            self.directory = ['']
            self.directory.extend(dir.split('.'))
        except KeyError:
            dirappend = [ time.strftime("%Y%b%d",localtime) ,time.strftime("%H%M_%S", localtime)]
            self.datasetNameAppend = time.strftime("%Y%b%d_%H%M_%S",localtime)
            
            blue_scan_append = ['bsb_scan']
            red_scan_append = ['rsb_scan']
            blue_flop_append = ['bsb_flop']
            red_flop_append = ['rsb_flop']
            directory = ['','Experiments']
            directory.extend([self.name])
            directory.extend(dirappend)
            
            self.bsb_scan_dir = []
            self.rsb_scan_dir = []
            self.bsb_flop_dir = []
            self.rsb_flop_dir = []
            
            self.bsb_scan_dir.extend(directory)
            self.bsb_scan_dir.extend(blue_scan_append)

            self.rsb_scan_dir.extend(directory)
            self.rsb_scan_dir.extend(red_scan_append)

            self.bsb_flop_dir.extend(directory)
            self.bsb_flop_dir.extend(blue_flop_append)

            self.rsb_flop_dir.extend(directory)
            self.rsb_flop_dir.extend(red_flop_append)
            
    def setup_scan(self, sideband):

        if sideband == 'blue':
                       
            replace = TreeDict.fromdict({
                    'Spectrum.sensitivity_selection':'temperature',
                    'Spectrum.scan_selection':'auto',
                    'Spectrum.sideband_selection':self.bsb_sel,
                    'Spectrum.save_directory': self.bsb_scan_dir,
                    'Spectrum.dataset_name_append':self.datasetNameAppend,
                    'Spectrum.window_name': ['Blue sideband scan']
                    })

            self.spectrum.set_parameters(replace)

        elif sideband == 'red':
            temp = self.parameters.Temperature

            replace = TreeDict.fromdict({
                    'Spectrum.sensitivity_selection': 'temperature',
                    'Spectrum.scan_selection': 'auto',
                    'Spectrum.sideband_selection':self.rsb_sel,
                    'Spectrum.save_directory': self.rsb_scan_dir,
                    'Spectrum.dataset_name_append': self.datasetNameAppend,
                    'Spectrum.window_name': ['Red sideband scan']
                    })

            self.spectrum.set_parameters(replace)

    def setup_flop(self, sideband):
        if sideband == 'blue':
            replace = TreeDict.fromdict({
                    'RabiFlopping.sideband_selection':self.bsb_sel,
                    'RabiFlopping.window_name': ['Blue sideband Rabi flop'],
                    'RabiFlopping.save_directory': self.bsb_flop_dir,
                    'RabiFlopping.dataset_name_append': self.datasetNameAppend
                    })

            self.flop.set_parameters(replace)

        if sideband == 'red':
            replace = TreeDict.fromdict({
                    'RabiFlopping.sideband_selection':self.rsb_sel,
                    'RabiFlopping.window_name': ['Red sideband Rabi flop'],
                    'RabiFlopping.save_directory': self.rsb_flop_dir,
                    'RabiFlopping.dataset_name_append': self.datasetNameAppend
                    })

            self.flop.set_parameters(replace)
            

    def update_frequency(self, sideband_frequency):
        '''
        Obtain the frequency of the sideband. Update the parameter vault and the
        script parameters with the new value
        '''
        sp = self.parameters.Spectrum
        line = self.drift_tracker.get_current_line(sp.line_selection)
        trap_frequency = abs( sideband_frequency - line )
        self.pv.set_parameter('TrapFrequencies', self.mode, trap_frequency)
        collection = 'TrapFrequencies.' + self.mode
        replace = TreeDict.fromdict({
                collection: trap_frequency
                })

    def update_excitation_time(self, t):
        '''
        Update the excitation time of the frequency scans to the
        pi time on the blue sideband rabi flop
        '''
        sp = self.parameters.Spectrum
        span, resolution, duration, amplitude = sp['temperature']
        duration = t
        sp['Temperature'] = (span, resolution, duration, amplitude)
    
    def run(self, cxn, context):
        '''
        General procedure is:
        rabi flop bsb --> extract pi time
        set excitation time to pi time
        scan over blue sideban with pi time excitation
        scan over red sideband with pi time excitation
        optional: also flop red sideband
        '''

        self.setup_flop('blue')
        self.flop.set_progress_limits(0., 33.)
        pi_time = self.flop.run(cxn, context)
        if self.flop.should_stop: return
        self.update_excitation_time(pi_time)
        self.setup_scan('blue')
        self.spectrum.set_progress_limits(33., 66.)
        (center, fwhm, blue_height) = self.spectrum.run(cxn, context)
        if self.spectrum.should_stop: return
        self.update_frequency(center) # update the stored frequencies
        self.setup_scan('red')
        self.spectrum.set_progress_limits(66., 100.)
        (center, fwhm, red_height) = self.spectrum.run(cxn, context)
        if self.spectrum.should_stop: return
        r = red_height/blue_height
        nbar = r/(1. - r)
        print "nbar: " + str(nbar)
        print nbar
        return nbar # average motional excitation from sideband heights

    def finalize(self, cxn, context):
        #self.save_parameters(self.dv, cxn, self.cxnlab, self.temp_save_context)
        self.spectrum.finalize(cxn, context)
        self.flop.finalize(cxn, context)
        pass

    def save_parameters(self, dv, cxn, cxnlab, context):
        measuredDict = dvParameters.measureParameters(cxn, cxnlab)
        dvParameters.saveParameters(dv, measuredDict, context)
        dvParameters.saveParameters(dv, dict(self.parameters), context)

if __name__ == '__main__':
    import labrad
    cxn = labrad.connect()
    scanner = cxn.scriptscanner
    exprt = temperature(cxn = cxn)
    ident = scanner.register_external_launch(exprt.name)
    exprt.execute(ident)
