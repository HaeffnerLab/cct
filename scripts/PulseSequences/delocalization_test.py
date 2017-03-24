from common.okfpgaservers.pulser.pulse_sequences.pulse_sequence import pulse_sequence
from subsequences.RepumpD import repump_d
from subsequences.DopplerCooling import doppler_cooling
from subsequences.EmptySequence import empty_sequence
from subsequences.OpticalPumping import optical_pumping
from subsequences.RabiExcitation import rabi_excitation_select_channel
from subsequences.TurnOffAll import turn_off_all
from subsequences.SidebandCooling import sideband_cooling
from subsequences.voltage_ramp import ramp_voltage
from subsequences.reset_dac import reset_dac
from subsequences.StateReadout import state_readout
from labrad.units import WithUnit
from treedict import TreeDict

class delocalization_test(pulse_sequence):
    
    required_parameters = [ 
                           ('Heating', 'background_heating_time'),
                           ('OpticalPumping','optical_pumping_enable'), 
                           ('SidebandCooling','sideband_cooling_enable'),
                           ]
    
    required_subsequences = [repump_d, doppler_cooling, empty_sequence, optical_pumping, 
                             rabi_excitation_select_channel, turn_off_all, sideband_cooling, ramp_voltage, 
                             reset_dac, state_readout]
    
    replaced_parameters = {empty_sequence:[('EmptySequence','empty_sequence_duration'),]}

    def sequence(self):
        p = self.parameters
        self.end = WithUnit(10, 'us')

        self.addSequence(turn_off_all)
        
        self.addSequence(repump_d)
        
        self.addSequence(rabi_excitation_select_channel)
        
        self.addSequence(state_readout)        
        
        self.addSequence(empty_sequence, TreeDict.fromdict({'EmptySequence.empty_sequence_duration':WithUnit(10,'ms')})) ##state readout has 2ms hangover.  It shouldn't. Ask Dylan
        
        self.addSequence(doppler_cooling)
        if p.OpticalPumping.optical_pumping_enable:
            self.addSequence(optical_pumping)
        if p.SidebandCooling.sideband_cooling_enable:
            self.addSequence(sideband_cooling)

        self.addSequence(ramp_voltage)

        self.addSequence(empty_sequence, TreeDict.fromdict({'EmptySequence.empty_sequence_duration':p.Heating.background_heating_time}))
        
        self.addSequence(empty_sequence, TreeDict.fromdict({'EmptySequence.empty_sequence_duration':WithUnit(1,'us')}))
        
        self.addSequence(ramp_voltage)

        self.addSequence(state_readout)
        
        self.addSequence(reset_dac)
        
        #print self.parameters.Excitation_729.rabi_excitation_frequency
        #import IPython
        #IPython.embed()
        

