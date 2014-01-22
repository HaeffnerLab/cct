from common.okfpgaservers.pulser.pulse_sequences.pulse_sequence import pulse_sequence
from OpticalPumpingContinuous import optical_pumping_continuous
from OpticalPumpingPulsed import optical_pumping_pulsed
from treedict import TreeDict

class optical_pumping_with_mode_swapping(pulse_sequence):
    
    
    required_parameters = [
                  ('OpticalPumping','optical_pumping_type'),
                  ('OpticalPumping','optical_pumping_frequency_729'),
                  ('OpticalPumping','optical_pumping_frequency_854'),
                  ('OpticalPumping','optical_pumping_frequency_866'),
                  ('OpticalPumping','optical_pumping_amplitude_729'),
                  ('OpticalPumping','optical_pumping_amplitude_854'),
                  ('OpticalPumping','optical_pumping_amplitude_866'),
                  ('OpticalPumpingContinuous','optical_pumping_continuous_duration'),
                  ('OpticalPumpingContinuous','optical_pumping_continuous_repump_additional'),
                  ('ParametricCoupling', 'mode_swapping_time')
                  ]
    
    required_subsequences = [optical_pumping_continuous, optical_pumping_pulsed]
    
    def sequence(self):
        op = self.parameters.OpticalPumping
        opc = self.parameters.OpticalPumpingContinuous
        
        if op.optical_pumping_type == 'continuous':
            continuous = True
        elif op.optical_pumping_type == 'pulsed':
            continuous = False
        else:
            raise Exception ('Incorrect optical pumping type {0}'.format(op.optical_pumping_type))
        if continuous:
            replace = {
                       'OpticalPumpingContinuous.optical_pumping_continuous_frequency_854':op.optical_pumping_frequency_854,
                       'OpticalPumpingContinuous.optical_pumping_continuous_amplitude_854':op.optical_pumping_amplitude_854,
                       'OpticalPumpingContinuous.optical_pumping_continuous_frequency_729':op.optical_pumping_frequency_729,
                       'OpticalPumpingContinuous.optical_pumping_continuous_amplitude_729':op.optical_pumping_amplitude_729,
                       'OpticalPumpingContinuous.optical_pumping_continuous_frequency_866':op.optical_pumping_frequency_866,
                       'OpticalPumpingContinuous.optical_pumping_continuous_amplitude_866':op.optical_pumping_amplitude_866,
                       }
            self.addSequence(optical_pumping_continuous, TreeDict.fromdict(replace))
            opc_dur = opc.optical_pumping_continuous_duration
            self.addTTL('parametric_modulation', self.start + opc_dur , self.parameters.ParametricCoupling.mode_swapping_time)
            #print opc.optical_pumping_continuous_duration
            self.end = self.start + max(opc_dur + opc.optical_pumping_continuous_repump_additional, opc_dur + self.parameters.ParametricCoupling.mode_swapping_time)

        else:
            #pulsed
            replace = {
                       'OpticalPumpingPulsed.optical_pumping_pulsed_frequency_854':op.optical_pumping_frequency_854,
                       'OpticalPumpingPulsed.optical_pumping_pulsed_amplitude_854':op.optical_pumping_amplitude_854,
                       'OpticalPumpingPulsed.optical_pumping_pulsed_frequency_729':op.optical_pumping_frequency_729,
                       'OpticalPumpingPulsed.optical_pumping_pulsed_amplitude_729':op.optical_pumping_amplitude_729,
                       'OpticalPumpingPulsed.optical_pumping_pulsed_frequency_866':op.optical_pumping_frequency_866,
                       'OpticalPumpingPulsed.optical_pumping_pulsed_amplitude_866':op.optical_pumping_amplitude_866,
                       }
            self.addSequence(optical_pumping_pulsed, TreeDict.fromdict(replace))