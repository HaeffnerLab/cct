from __future__ import division
from common.abstractdevices.script_scanner.scan_methods import experiment
from spectrum import spectrum
from rabi_flopping import rabi_flopping
from temperature import temperature
from labrad.units import WithUnit
from treedict import TreeDict
import time
import labrad
'''
General experiment to measure heating rate of a mode
'''


class heating_rate(experiment):

    name = 'HeatingRate'

    required_parameters = [ 
        ('Spectrum', 'temperature'), # sensitivity selection for heating rate scan
        
        ('Temperature', 'mode'),
        #('Temperature', 'autofit_spectrum'),
        #('Temperature', 'rabi_flop_rsb'),
        
        ('HeatingRate', 'rabi_flop_enable'),
        ('HeatingRate', 'heating_scan'), #(min_time, max_time, number of steps)
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

        self.nbars = []
        self.do_flop = self.parameters.HeatingRate.rabi_flop_enable
        (min_time, max_time,num_steps) = self.parameters.HeatingRate.heating_scan
        min_time = min_time['ms']; max_time = max_time['ms']
        step_size = (max_time-min_time)/num_steps
        self.heating_times = [i*step_size for i in range(int(min_time),int(max_time/step_size))]
        
        
        # write the red and blue sideband scan selections in a form that the drift
        # tracker will recognize
        self.rsb_sel = [0, 0, 0, 0]
        self.bsb_sel = [0, 0, 0, 0]
        j = ['radial_frequency_1', 'radial_frequency_2', 'axial_frequency'].index(self.mode)
        self.rsb_sel[j] = -1
        self.bsb_sel[j] = 1

        self.spectrum = self.make_experiment(spectrum)
        self.flop = self.make_experiment(rabi_flopping)
        self.temperature = self.make_experiment(temperature)
        self.temperature.initialize(cxn, context, ident)
        self.spectrum.initialize(cxn, context, ident)
        self.temp_save_context = cxn.context()
        self.flop.initialize(cxn, context, ident)
        
        self.setup_data_vault_dirs()

    def setup_data_vault_dirs(self):
        localtime = time.localtime()
        try:
            direc = self.parameters.get('HeatingRate.save_directory') #ask about this
            self.directory = ['']
            self.directory.extend(direc.split('.'))
        except KeyError:
            dirappend = [ time.strftime("%Y%b%d",localtime) ,time.strftime("%H%M_%S", localtime)]
            self.datasetNameAppend = time.strftime("%Y%b%d_%H%M_%S",localtime)

            directory = ['','Experiments']
            directory.extend([self.name])
            directory.extend(dirappend)
            
            blue_flop_append = ['bsb_flop']
            red_flop_append = ['rsb_flop']
            
            self.bsb_flop_dir = []
            self.rsb_flop_dir = []
            
            self.bsb_flop_dir.extend(directory)
            self.bsb_flop_dir.extend(blue_flop_append)

            self.rsb_flop_dir.extend(directory)
            self.rsb_flop_dir.extend(red_flop_append)

            self.temp_save_dir = []
            self.temp_save_dir.extend(directory)
           # self.temp_save_dir.extend(str(heatingtime))

            self.save_directory = directory
            self.dv.cd(self.save_directory ,True, context = self.temp_save_context)
            self.dv.new('HeatingRate {}'.format(self.datasetNameAppend),[('Heating Time', 'ms')],[('nbar','Arb','Arb')], context = self.temp_save_context)
            self.dv.add_parameter('Window', self.name, context = self.temp_save_context)
            self.dv.add_parameter('plotLive', True, context = self.temp_save_context)
            
    def setup_temp(self, t):
        replace = TreeDict.fromdict({
                'Temperature.save_directory': self.temp_save_dir,
                'Heating.background_heating_time':t #does this need units?
                })
        self.temperature.set_parameters(replace)

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
        
        '''Heating Rate procedure:
        check boolean - do rabi flop
        iterate: setup_temp with new heating_time
        store/plot nbar values
        

        '''
        
        if self.do_flop:
            self.setup_flop('blue')
            self.flop.set_progress_limits(0., 10.) 
            pi_time = self.flop.run(cxn, context)
            if self.flop.should_stop: return
            self.update_excitation_time(pi_time)

        self.spectrum.set_progress_limits(10., 75.) #scale this?
        
        for t in self.heating_times:
            self.setup_temp(t)
            nbar = self.temperature.run(cxn, context) 
            self.nbars.append(nbar)
            self.dv.add([t,nbar])
            if self.spectrum.should_stop: return
        
        print self.heating_times
        print self.nbars
        return self.nbars #add this to datavault
            

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
    exprt = heating_rate(cxn = cxn)
    ident = scanner.register_external_launch(exprt.name)
    exprt.execute(ident)
