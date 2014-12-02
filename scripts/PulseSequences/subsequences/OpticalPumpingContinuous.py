from common.okfpgaservers.pulser.pulse_sequences.pulse_sequence import pulse_sequence

class optical_pumping_continuous(pulse_sequence):
    
    
    required_parameters = [
                  ('OpticalPumpingContinuous','optical_pumping_continuous_duration'),
                  ('OpticalPumpingContinuous','optical_pumping_continuous_repump_additional'),
                  ('OpticalPumpingContinuous','optical_pumping_continuous_frequency_854'),
                  ('OpticalPumpingContinuous','optical_pumping_continuous_amplitude_854'),
                  ('OpticalPumpingContinuous','optical_pumping_continuous_frequency_729'),
                  ('OpticalPumpingContinuous','optical_pumping_continuous_amplitude_729'),
                  ('OpticalPumpingContinuous','optical_pumping_continuous_frequency_866'), 
                  ('OpticalPumpingContinuous','optical_pumping_continuous_amplitude_866'),
                  ('OpticalPumpingContinuous', 'beam'),

                  ]

    def sequence(self):
        opc = self.parameters.OpticalPumpingContinuous
        repump_dur_854 = opc.optical_pumping_continuous_duration + opc.optical_pumping_continuous_repump_additional
        repump_dur_866 = opc.optical_pumping_continuous_duration + 2 * opc.optical_pumping_continuous_repump_additional
        self.end = self.start + repump_dur_866
        print opc
        #if not opc.pumping_2_ions:
        self.addDDS('729', self.start, opc.optical_pumping_continuous_duration, opc.optical_pumping_continuous_frequency_729, opc.optical_pumping_continuous_amplitude_729)
        self.addTTL(opc.beam, self.start, opc.optical_pumping_continuous_duration)
        print 'op:', opc.optical_pumping_continuous_frequency_729
        self.addDDS('854', self.start, repump_dur_854, opc.optical_pumping_continuous_frequency_854, opc.optical_pumping_continuous_amplitude_854)
        self.addDDS('866', self.start, repump_dur_866, opc.optical_pumping_continuous_frequency_866, opc.optical_pumping_continuous_amplitude_866)
# class optical_pumping_continuous(pulse_sequence):
#     
#     
#     required_parameters = [
#                   ('OpticalPumpingContinuous','optical_pumping_continuous_duration'),
#                   ('OpticalPumpingContinuous','optical_pumping_continuous_repump_additional'),
#                   ('OpticalPumpingContinuous','optical_pumping_continuous_frequency_854'),
#                   ('OpticalPumpingContinuous','optical_pumping_continuous_amplitude_854'),
#                   ('OpticalPumpingContinuous','optical_pumping_continuous_frequency_729'),
#                   ('OpticalPumpingContinuous','optical_pumping_continuous_amplitude_729'),
#                   ('OpticalPumpingContinuous','optical_pumping_continuous_frequency_866'), 
#                   ('OpticalPumpingContinuous','optical_pumping_continuous_amplitude_866'),
#             
#                   ]
# 
#     def sequence(self):
#         opc = self.parameters.OpticalPumpingContinuous
#         repump_dur_854 = opc.optical_pumping_continuous_duration + opc.optical_pumping_continuous_repump_additional
#         repump_dur_866 = opc.optical_pumping_continuous_duration + 2 * opc.optical_pumping_continuous_repump_additional
#         self.end = self.start + repump_dur_866
#         self.addDDS('729', self.start, opc.optical_pumping_continuous_duration, opc.optical_pumping_continuous_frequency_729, opc.optical_pumping_continuous_amplitude_729)
#         self.addDDS('854', self.start, repump_dur_854, opc.optical_pumping_continuous_frequency_854, opc.optical_pumping_continuous_amplitude_854)
#         self.addDDS('866', self.start, repump_dur_866, opc.optical_pumping_continuous_frequency_866, opc.optical_pumping_continuous_amplitude_866)