from common.okfpgaservers.pulser.pulse_sequences.pulse_sequence import pulse_sequence
from subsequences.RepumpDwithDoppler import doppler_cooling_after_repump_d
from subsequences.RepumpDwithDopplerAndModeCoupling import doppler_cooling_with_mode_coupling
from subsequences.EmptySequence import empty_sequence
from subsequences.OpticalPumping import optical_pumping
from subsequences.RabiExcitation import rabi_excitation
from subsequences.Tomography import tomography_readout
from subsequences.StateReadout import state_readout
from subsequences.TurnOffAll import turn_off_all
from subsequences.SidebandCooling import sideband_cooling
from subsequences.WireCharging import wire_charging
from subsequences.PulsedHeating import pulsed_heating
from subsequences.PiPulse import pi_pulse
from subsequences.RepumpD import repump_d
from subsequences.ParametricCoupling import parametric_coupling
from labrad.units import WithUnit
from treedict import TreeDict

class mode_coupling(pulse_sequence):
    
    required_parameters =  [
                            ('Heating', 'background_heating_time'),
                            ('OpticalPumping','optical_pumping_enable'), 
                            ('SidebandCooling','sideband_cooling_enable'),
                            ('SidebandPrecooling','sideband_precooling_enable'),
                            
                            ('RepumpD_5_2','repump_d_duration'),
                            ('RepumpD_5_2','repump_d_frequency_854'),
                            ('RepumpD_5_2','repump_d_amplitude_854'),
                            ('DopplerCooling', 'doppler_cooling_frequency_397'),
                            ('DopplerCooling', 'doppler_cooling_amplitude_397'),
                            ('DopplerCooling', 'doppler_cooling_frequency_866'),
                            ('DopplerCooling', 'doppler_cooling_amplitude_866'),
                            ('DopplerCooling', 'doppler_cooling_repump_additional'),
                            ('DopplerCooling', 'doppler_cooling_duration'),
                            ('DopplerCooling', 'mode_swapping_cycles'),
                            ('DopplerCooling', 'mode_swapping_enable'),

                            ('OpticalPumping','optical_pumping_frequency_729'),
                            ('OpticalPumping','optical_pumping_frequency_854'),
                            ('OpticalPumping','optical_pumping_frequency_866'),
                            ('OpticalPumping','optical_pumping_amplitude_729'),
                            ('OpticalPumping','optical_pumping_amplitude_854'),
                            ('OpticalPumping','optical_pumping_amplitude_866'),
                            ('OpticalPumping','optical_pumping_type'),
                          
                            ('OpticalPumpingContinuous','optical_pumping_continuous_duration'),
                            ('OpticalPumpingContinuous','optical_pumping_continuous_repump_additional'),
                          
                            ('OpticalPumpingPulsed','optical_pumping_pulsed_cycles'),
                            ('OpticalPumpingPulsed','optical_pumping_pulsed_duration_729'),
                            ('OpticalPumpingPulsed','optical_pumping_pulsed_duration_repumps'),
                            ('OpticalPumpingPulsed','optical_pumping_pulsed_duration_additional_866'),
                            ('OpticalPumpingPulsed','optical_pumping_pulsed_duration_between_pulses'),
            
                            ('SidebandCooling','sideband_cooling_cycles'),
                            ('SidebandCooling','sideband_cooling_type'),
                            ('SidebandCooling','sideband_cooling_duration_729_increment_per_cycle'),
                            ('SidebandCooling','sideband_cooling_frequency_854'),
                            ('SidebandCooling','sideband_cooling_amplitude_854'),
                            ('SidebandCooling','sideband_cooling_frequency_866'),
                            ('SidebandCooling','sideband_cooling_amplitude_866'),
                            ('SidebandCooling','sideband_cooling_frequency_729'),
                            ('SidebandCooling','sideband_cooling_amplitude_729'),
                            ('SidebandCooling','sideband_cooling_optical_pumping_duration'),
                            ('SidebandCooling', 'sideband_cooling_detuning_729'),

                            ('SidebandPrecooling','sideband_precooling_cycles'),
                            ('SidebandPrecooling','sideband_precooling_optical_pumping_duration'),
                            ('SidebandPrecooling','sideband_precooling_amplitude_866'),
                            ('SidebandPrecooling','sideband_precooling_amplitude_854'),
                            ('SidebandPrecooling','sideband_precooling_amplitude_729'),
                            ('SidebandPrecooling','sideband_precooling_frequency_854'),
                            ('SidebandPrecooling', 'sideband_precooling_frequency_866'),
                            ('SidebandPrecooling', 'sideband_precooling_frequency_729'),
                            ('SidebandPrecooling', 'sideband_precooling_detuning_729'),
                            ('SidebandPrecooling','sideband_precooling_continuous_duration'),
            
                            
                            ('SidebandCoolingContinuous','sideband_cooling_continuous_duration'),
                          
                            ('SidebandCoolingPulsed','sideband_cooling_pulsed_duration_729'),
                            ('SidebandCoolingPulsed','sideband_cooling_pulsed_cycles'),
                            ('SidebandCoolingPulsed','sideband_cooling_pulsed_duration_repumps'),
                            ('SidebandCoolingPulsed','sideband_cooling_pulsed_duration_additional_866'),
                            ('SidebandCoolingPulsed','sideband_cooling_pulsed_duration_between_pulses'),
                          
                            ('Excitation_729','rabi_excitation_frequency'),
                            ('Excitation_729','rabi_excitation_amplitude'),
                            ('Excitation_729','rabi_excitation_duration'),
                            ('Excitation_729','rabi_excitation_phase'),

                            ('PiPulse', 'pi_time'),
                            ('PiPulse', 'rabi_amplitude_729'),
                            ('PiPulse', 'rabi_excitation_frequency'),

                            ('ParametricCoupling', 'parametric_coupling_duration'),
                            ('ParametricCoupling', 'mode_swapping_time'),

                            ('StateReadout','state_readout_frequency_397'),
                            ('StateReadout','state_readout_amplitude_397'),
                            ('StateReadout','state_readout_frequency_866'),
                            ('StateReadout','state_readout_amplitude_866'),
                            ('StateReadout','state_readout_duration'),
                            
                            #('Tomography', 'rabi_pi_time'),
                            #('Tomography', 'iteration'),
                            #('Tomography', 'tomography_excitation_frequency'),
                            #('Tomography', 'tomography_excitation_amplitude'),
                            ]
    
    
    required_subsequences = [doppler_cooling_after_repump_d, doppler_cooling_with_mode_coupling, empty_sequence, optical_pumping, 
                             rabi_excitation, state_readout, turn_off_all,  sideband_cooling, pi_pulse,
                             repump_d, parametric_coupling]

    def sequence(self):
        p = self.parameters
        self.end = WithUnit(10, 'us')
        self.addSequence(turn_off_all)
        if p.DopplerCooling.mode_swapping_enable:
            self.addSequence(doppler_cooling_with_mode_coupling)
        else:
            self.addSequence(doppler_cooling_after_repump_d)
        if p.OpticalPumping.optical_pumping_enable:
            self.addSequence(optical_pumping)
        if p.SidebandCooling.sideband_cooling_enable:
            self.addSequence(sideband_cooling)
        self.addSequence(pi_pulse)
        self.addSequence(repump_d)
        self.addSequence(optical_pumping)
        self.addSequence(parametric_coupling)
        self.addSequence(empty_sequence, TreeDict.fromdict({'EmptySequence.empty_sequence_duration':p.Heating.background_heating_time}))
        self.start_excitation_729 = self.end
        self.addSequence(rabi_excitation)
        self.addSequence(state_readout)
