from cct.scripts.PulseSequences.mode_coupling import mode_coupling
from excitation_729 import excitation_729

class excitation_mode_coupling(excitation_729):
    
    name = 'ExcitationModeCoupling'
    
    required_parameters = [('OpticalPumping','frequency_selection'),
                           ('OpticalPumping','manual_frequency_729'),
                           ('OpticalPumping','line_selection'),
                           
                           ('SidebandCooling','frequency_selection'),
                           ('SidebandCooling','manual_frequency_729'),
                           ('SidebandCooling','line_selection'),
                           ('SidebandCooling','sideband_selection'),

                           ('SidebandPrecooling', 'frequency_selection'),
                           ('SidebandPrecooling', 'manual_frequency_729'),
                           ('SidebandPrecooling', 'sideband_selection'),
                           ('TrapFrequencies','axial_frequency'),
                           ('TrapFrequencies','radial_frequency_1'),
                           ('TrapFrequencies','radial_frequency_2'),
                           ('TrapFrequencies','rf_drive_frequency'),
                           
                           ('StateReadout', 'repeat_each_measurement'),
                           ('StateReadout', 'state_readout_threshold'),
                           ('Excitation_729', 'lock_excitation_phase'),
                           ('Excitation_729', 'phase_delay')
                           ]
    pulse_sequence = mode_coupling
    required_parameters.extend(pulse_sequence.required_parameters)
    #removing pulse sequence items that will be calculated in the experiment and do not need to be loaded
    required_parameters.remove(('OpticalPumping', 'optical_pumping_frequency_729'))
    required_parameters.remove(('SidebandCooling', 'sideband_cooling_frequency_729'))
    required_parameters.remove(('SidebandPrecooling', 'sideband_precooling_frequency_729'))
if __name__ == '__main__':
    import labrad
    cxn = labrad.connect()
    scanner = cxn.scriptscanner
    exprt = excitation_ramsey(cxn = cxn)
    ident = scanner.register_external_launch(exprt.name)
    exprt.execute(ident)