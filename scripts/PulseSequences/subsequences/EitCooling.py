from common.okfpgaservers.pulser.pulse_sequences.pulse_sequence import pulse_sequence
from labrad.units import WithUnit
from treedict import TreeDict

class eit_cooling(pulse_sequence):
    
    required_parameters = [
                           ('StatePreparation','channel_397_sigma'),
                           ('StatePreparation','channel_397_linear'),
                           
                           ('DopplerCooling','doppler_cooling_frequency_397'),
                           
                           ('EitCooling','eit_cooling_amplitude_397_sigma'),
                           ('EitCooling','eit_cooling_amplitude_397_linear'),
                           ('EitCooling','eit_cooling_amplitude_866'),
                           ('EitCooling','eit_cooling_frequency_866'),
                           ('EitCooling','eit_cooling_delta'),
                           ('EitCooling','eit_cooling_zeeman_splitting'),  #maybe this should be calculated later with the B field?
                           ('EitCooling','eit_cooling_duration')                                                      
                           ]
    
    replaced_parameters = {
                           }
    
    def sequence(self):
        '''
        EIT cooling subsequence consists of a pulse of low power linearly polarized 397 and high power sigma polarized 397 with 866 for repump.
        '''
        eit = self.parameters.EitCooling
        sp = self.parameters.StatePreparation

        if sp.channel_397_sigma == sp.channel_397_linear:
            raise Exception ("Circular and Linear Polarized 397 channels cannot be the same for EIT cooling")

        linewidth  = WithUnit(21.6, 'MHz')
        sigma_plus_resonance = self.parameters.DopplerCooling.doppler_cooling_frequency_397 + (linewidth/2.0 + eit.eit_cooling_zeeman_splitting/2.0)/2.0  #extra factor of two because AO shifts twice
        sigma_frequency = sigma_plus_resonance + eit.eit_cooling_delta/2.0 #extra factor of two because AO shifts twice
        linear_frequency = sigma_frequency - eit.eit_cooling_zeeman_splitting/2.0 #extra factor of two because AO shifts twice
        
        self.end = self.start + eit.eit_cooling_duration
        self.addDDS(sp.channel_397_sigma, self.start, eit.eit_cooling_duration, sigma_frequency, eit.eit_cooling_amplitude_397_sigma)
        self.addDDS(sp.channel_397_linear, self.start, eit.eit_cooling_duration, linear_frequency, eit.eit_cooling_amplitude_397_linear)
        self.addDDS('866', self.start, eit.eit_cooling_duration, eit.eit_cooling_frequency_866, eit.eit_cooling_amplitude_866)

