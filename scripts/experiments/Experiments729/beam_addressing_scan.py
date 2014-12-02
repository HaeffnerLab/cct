


from common.abstractdevices.script_scanner.scan_methods import experiment
from excitations import excitation_729
from cct.scripts.scriptLibrary.common_methods_729 import common_methods_729 as cm
from cct.scripts.scriptLibrary import dvParameters
import time
import labrad
from labrad.units import WithUnit
from numpy import linspace, arange
from IPython import embed

class beam_addressing_with_rabi_flop(experiment):
    
    name = 'Beam Addressing with Rabi Flop'
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
                           #('RabiFlopping_Sit', 'selected_ion'),
                           ('StateReadout', 'use_camera_for_readout'),
                           # Beam addressing scan parameters:
                           ('BeamAddressing','x_scan_parameters'), #Has min, max, steps. Zero is where the current position is.
                           ('BeamAddressing','y_scan_parameters'), #Has min, max, steps. Zero is where the current position is.
                           ('BeamAddressing','scan_y'),#Boolean
                           #('BeamAddressing','set_position'),
                                                     
                    
                           ]
    required_parameters.extend(trap_frequencies)
    
    @classmethod
    def all_required_parameters(cls):
        parameters = set(cls.required_parameters)
        parameters = parameters.union(set(cls.trap_frequencies))
        parameters = parameters.union(set(excitation_729.all_required_parameters()))
        parameters = list(parameters)
        #removing parameters we'll be overwriting, and they do not need to be loaded
        parameters.remove(('Excitation_729','rabi_excitation_amplitude'))
        parameters.remove(('Excitation_729','rabi_excitation_duration'))
        parameters.remove(('Excitation_729','rabi_excitation_frequency'))
        return parameters
    
    
    def initialize(self, cxn, context, ident):
        self.ident = ident
        self.excite = self.make_experiment(excitation_729)
        self.excite.initialize(cxn, context, ident)
        self.scan = []
        self.amplitude = None
        self.duration = None
        self.cxnlab = labrad.connect('192.168.169.49') #connection to labwide network
        
        self.cxn_apt_ip = '192.168.169.30' # ip address of APT motor server         
        #Define mirror motors and serial numbers (must be the same as in APT_config.py file in APT server directory):
        self.motors = [('729Mirror-XAxisCamera', 83849921), ('729Mirror-YAxisCamera', 83833535)] 
        self.position_limits = { '729Mirror-XAxisCamera' : (-1.3, 4.7), '729Mirror-YAxisCamera': (-2.4, 3.7)  }
        self.apt  = self.get_apt() 
        #check_motor_connections() 


        self.drift_tracker = cxn.sd_tracker
        self.dv = cxn.data_vault
        self.beam_addressing_with_rabi_flop_save_context = cxn.context()
    

    def setup_sequence_parameters(self):
        self.load_frequency()
        self.parameters['Excitation_729.rabi_excitation_amplitude'] = self.parameters.RabiFlopping.rabi_amplitude_729
        self.parameters['Excitation_729.rabi_excitation_duration'] = self.parameters.RabiFlopping_Sit.sit_on_excitation
       
        if self.parameters.BeamAddressing.scan_y:
            self.target_motor = self.motors[1][0] 
            self.select_motor()

            self.y_minim_WithUnits, self.y_maxim_WithUnits, self.y_scan_steps = self.parameters.BeamAddressing.y_scan_parameters
            self.y_minim = 0.000568*self.y_minim_WithUnits['um']; self.y_maxim = 0.000568*self.y_maxim_WithUnits['um']
            
            if not self.is_within_limits(self.y_minim, self.y_maxim):
                raise Exception('Input position range is not within motor limits!')
            
            if self.y_maxim - self.y_minim >= 0 and self.y_scan_steps > 0:
                #self.step_size  =  float( self.y_maxim - self.y_minim )/self.y_scan_steps
                self.scan_beam_window  =  linspace(self.y_minim, self.y_maxim, self.y_scan_steps)  
                
            else:
                raise Exception("Max y range is less than min y range!")
            
        else:
            self.target_motor = self.motors[0][0] 
            self.select_motor()

            self.x_minim_WithUnits, self.x_maxim_WithUnits, self.x_scan_steps = self.parameters.BeamAddressing.x_scan_parameters
            self.x_minim = 0.0011538*self.x_minim_WithUnits['um']; self.x_maxim = 0.0011538*self.x_maxim_WithUnits['um']
            
            if not self.is_within_limits(self.x_minim, self.x_maxim):
                raise Exception('Input position range is not within motor limits!')

            if self.x_maxim - self.x_minim >= 0 and self.x_scan_steps > 0:
                self.step_size  =  float( self.x_maxim - self.x_minim )/self.x_scan_steps
                self.scan_beam_window  =  linspace(self.x_minim, self.x_maxim, self.x_scan_steps)  
            else:
                raise Exception("Max x range is less than min x range!")
            

        
        

    def is_within_limits(self, rel_min, rel_max):
        '''
        Return False if relative min and max are within motor position limits.

        '''
        absolute_position = self.get_position()
        return ( absolute_position > self.position_limits[self.target_motor][0] ) and (  absolute_position < self.position_limits[self.target_motor][1] )


    def setup_data_vault(self):
        localtime = time.localtime()
        datasetNameAppend = time.strftime("%Y%b%d_%H%M_%S",localtime)
        dirappend = [ time.strftime("%Y%b%d",localtime) ,time.strftime("%H%M_%S", localtime)]
        directory = ['','Experiments']
        directory.extend([self.name])
        directory.extend(dirappend)
        self.dv.cd(directory ,True, context = self.beam_addressing_with_rabi_flop_save_context)
        output_size = self.excite.output_size
        dependants = [('Excitation','Ion {}'.format(ion),'Probability') for ion in range(output_size)]
        self.dv.new('Beam Addressing with Rabi Flopping {}'.format(datasetNameAppend),[('Position', 'um')], dependants , context = self.beam_addressing_with_rabi_flop_save_context)
        self.dv.add_parameter('Window', ['Beam Addressing with Rabi Flopping'], context = self.beam_addressing_with_rabi_flop_save_context)
        self.dv.add_parameter('plotLive', True, context = self.beam_addressing_with_rabi_flop_save_context)

    def load_frequency(self):
        #reloads trap frequencyies and gets the latest information from the drift tracker
        self.reload_some_parameters(self.trap_frequencies) 
        flop = self.parameters.RabiFlopping
        frequency = cm.frequency_from_line_selection(flop.frequency_selection, flop.manual_frequency_729, flop.line_selection, self.drift_tracker)
        trap = self.parameters.TrapFrequencies
        if flop.frequency_selection == 'auto':
            frequency = cm.add_sidebands(frequency, flop.sideband_selection, trap)
        self.parameters['Excitation_729.rabi_excitation_frequency'] = frequency
        
    def run(self, cxn, context):
        self.setup_data_vault()
        self.setup_sequence_parameters()
        self.load_frequency()
        self.excite.set_parameters(self.parameters)
        
        #Go to initial position:
        #self.apt.move_absolute(0.)
        self.init_position   =   self.get_position()
        for j in range(len(self.scan_beam_window)):
            should_stop = self.pause_or_stop()
            if should_stop: break
        
            self.move_absolute( self.scan_beam_window[j] )
        
            #Do Rabi flop with single excitation time:
            excitation, readouts  = self.excite.run(cxn, context)
            if not self.parameters['StateReadout.use_camera_for_readout']:
                single_excitation = excitation[0]
            else:
                #ion = int(self.parameters.RabiFlopping_Sit.selected_ion)
                ion = int(0)
                single_excitation = excitation[ion]
            
            #Send the position and data to the data_vault for plotting:
            if self.parameters.BeamAddressing.scan_y:
                position   = self.scan_beam_window[j]/0.000568
            else:
                position   = self.scan_beam_window[j]/0.0011538
            
            submission = [position]

            submission.extend(excitation)
            self.dv.add(submission, context = self.beam_addressing_with_rabi_flop_save_context)
            self.update_progress(j)
        self.cxn_apt.disconnect()
        #self.move_absolute( self.init_position )  #Move the motor back to where it started.
           
            
    def finalize(self, cxn, context):
        self.excite.finalize(cxn, context)
    
    def update_progress(self, iteration):
        progress = self.min_progress + (self.max_progress - self.min_progress) * float(iteration + 1.0) / len(self.scan_beam_window)
        self.sc.script_set_progress(self.ident,  progress)

    def get_apt(self):
        '''
        Connect to APT server and check for possible errors: 
        
        '''

        try:
            self.cxn_apt = labrad.connect(self.cxn_apt_ip)
            apt = self.cxn_apt.apt_motor_server
            return apt
        except Exception as inst:
            raise RuntimeError("Connection to {} could not be established: ".format(self.cxn_apt_ip) + str(inst))
    
    
    def check_motor_connections(self):
        '''
        check if the required motors are connected and if they recieve commands.
        
        '''
        try:
            available_motors = self.apt.get_available_devices()
        except Exception as inst:
            print "APT motor server was not found: " + inst           
 
        #Check if list of available motors contains mirror motors as defined (they are accessible):             
        for motor in self.motors: 
            if motor[0] not in available_motors:
                raise Exception("Motor {} was not found.".format(motor))
    
    def select_motor(self):
        self.apt.select_device(self.target_motor)

    def get_position(self):
        return self.apt.get_position()


    def move_relative(self, rel_position):
        self.apt.move_relative(rel_position)
    
    def move_absolute(self, absolute_position):
        self.apt.move_absolute(absolute_position)




        
if __name__ == '__main__':
    cxn = labrad.connect()
    scanner = cxn.scriptscanner
    exprt = beam_addressing_with_rabi_flop(cxn = cxn)
    ident = scanner.register_external_launch(exprt.name)
    exprt.execute(ident)



