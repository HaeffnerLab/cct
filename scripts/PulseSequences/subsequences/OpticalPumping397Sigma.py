from common.okfpgaservers.pulser.pulse_sequences.pulse_sequence import pulse_sequence

class optical_pumping_397sigma(pulse_sequence):
    
    
    required_parameters = [
                  ('OpticalPumping397Sigma','optical_pumping_397sigma_duration'),
                  ('OpticalPumping397Sigma','optical_pumping_397sigma_repump_additional'),
                  
                  ('OpticalPumping397Sigma','optical_pumping_397sigma_frequency_397'),
                  ('OpticalPumping397Sigma','optical_pumping_397sigma_amplitude_397'),
                  ('OpticalPumping397Sigma','optical_pumping_397sigma_frequency_866'), 
                  ('OpticalPumping397Sigma','optical_pumping_397sigma_amplitude_866'),
                  
                  ('StatePreparation','channel_397_sigma')
                  ]

    def sequence(self):
        ops = self.parameters.OpticalPumping397Sigma
        channel_397 = self.parameters.StatePreparation.channel_397_sigma

        repump_dur_866 = ops.optical_pumping_397sigma_duration + ops.optical_pumping_397sigma_repump_additional
        self.end = self.start + repump_dur_866
        self.addDDS(channel_397, self.start, ops.optical_pumping_397sigma_duration, ops.optical_pumping_397sigma_frequency_397, ops.optical_pumping_397sigma_amplitude_397)
        #print 'op:', ops.optical_pumping_397sigma_frequency_397
        self.addDDS('866', self.start, repump_dur_866, ops.optical_pumping_397sigma_frequency_866, ops.optical_pumping_397sigma_amplitude_866)
