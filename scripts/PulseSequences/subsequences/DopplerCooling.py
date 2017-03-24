from common.okfpgaservers.pulser.pulse_sequences.pulse_sequence import pulse_sequence 

class doppler_cooling(pulse_sequence):
    
    
    required_parameters = [
                           ('StatePreparation','channel_397_linear'),
                           ('StatePreparation','channel_397_sigma'),
                           
                           ('DopplerCooling','doppler_cooling_frequency_397'), 
                           ('DopplerCooling','doppler_cooling_amplitude_397'), 
                           ('DopplerCooling','doppler_cooling_frequency_866'), 
                           ('DopplerCooling','doppler_cooling_amplitude_866'), 
                           ('DopplerCooling','doppler_cooling_duration'),
                           ('DopplerCooling','doppler_cooling_repump_additional'),
                           ('DopplerCooling','doppler_cooling_include_second_397'),
                           ('DopplerCooling','doppler_cooling_frequency_397Extra'), 
                           ('DopplerCooling','doppler_cooling_amplitude_397Extra') 
                           ]
    
    def sequence(self):
        p = self.parameters.DopplerCooling
        sp = self.parameters.StatePreparation
        linear_397 = sp.channel_397_linear
        sigma_397 = sp.channel_397_sigma
        repump_duration = p.doppler_cooling_duration + p.doppler_cooling_repump_additional

        self.addDDS (linear_397,self.start, p.doppler_cooling_duration, p.doppler_cooling_frequency_397, p.doppler_cooling_amplitude_397)
        self.addDDS ('866',self.start, repump_duration, p.doppler_cooling_frequency_866, p.doppler_cooling_amplitude_866)
        if p.doppler_cooling_include_second_397:
            self.addDDS (sigma_397,self.start, p.doppler_cooling_duration, p.doppler_cooling_frequency_397Extra, p.doppler_cooling_amplitude_397Extra)
        self.end = self.start + repump_duration

