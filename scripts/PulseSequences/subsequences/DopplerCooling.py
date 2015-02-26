from common.okfpgaservers.pulser.pulse_sequences.pulse_sequence import pulse_sequence 

class doppler_cooling(pulse_sequence):
    
    
    required_parameters = [
                           ('DopplerCooling','doppler_cooling_frequency_397'), 
                           ('DopplerCooling','doppler_cooling_amplitude_397'),
                           ('DopplerCooling', 'doppler_cooling_frequency_397_2'),
                           ('DopplerCooling', 'doppler_cooling_amplitude_397_2'),
                           ('DopplerCooling','doppler_cooling_frequency_866'), 
                           ('DopplerCooling','doppler_cooling_amplitude_866'), 
                           ('DopplerCooling','doppler_cooling_duration'),
                           ('DopplerCooling','doppler_cooling_repump_additional'),
                           ('DopplerCooling', 'mode_swapping_enable'),
                           ('ParametricCoupling', 'drive_amplitude'),
                           ('ParametricCoupling', 'drive_frequency'),
                           ]
    
    def sequence(self):
        p = self.parameters.DopplerCooling
        pc = self.parameters.ParametricCoupling
        repump_duration = p.doppler_cooling_duration + p.doppler_cooling_repump_additional
        self.addDDS('397',self.start, p.doppler_cooling_duration, p.doppler_cooling_frequency_397, p.doppler_cooling_amplitude_397)
        self.addDDS('397_2',self.start, p.doppler_cooling_duration, p.doppler_cooling_frequency_397_2, p.doppler_cooling_amplitude_397_2)

        self.addDDS('866',self.start, repump_duration, p.doppler_cooling_frequency_866, p.doppler_cooling_amplitude_866)
        
        ##### TURN THE RF BIAS OFF DURING DOPPLER COOLING #########
        if p.mode_swapping_enable:
          self.addTTL('bias', self.start, p.doppler_cooling_duration)

        #if p.mode_swapping_enable:
        #  self.addDDS('parametric_coupling', self.start, p.doppler_cooling_duration, pc.drive_frequency, pc.drive_amplitude)
        self.end = self.start + repump_duration