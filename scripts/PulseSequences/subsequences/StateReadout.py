from common.okfpgaservers.pulser.pulse_sequences.pulse_sequence import pulse_sequence
from space_time.scripts.PulseSequences.subsequences.DopplerCooling import doppler_cooling
from treedict import TreeDict

class state_readout(pulse_sequence):
    '''
    Pulse sequence for reading out the state of the ion. 
    '''
    required_parameters = [
                           ('StateReadout','state_readout_frequency_397'), 
                           ('StateReadout','state_readout_amplitude_397'), 
                           ('StateReadout','state_readout_frequency_866'), 
                           ('StateReadout','state_readout_amplitude_866'), 
                           ('StateReadout','state_readout_duration'),
                           ('StateReadout','use_camera_for_readout'),
                           ('StateReadout','camera_trigger_width'),
                           ('StateReadout','camera_transfer_additional'),
                           ('StateReadout','state_readout_include_second_397'),
                           ]

    required_subsequences = [doppler_cooling]
    replaced_parameters = {
                          doppler_cooling:  [('DopplerCooling','doppler_cooling_frequency_397'),
                                             ('DopplerCooling','doppler_cooling_amplitude_397'),
                                             ('DopplerCooling','doppler_cooling_frequency_866'),
                                             ('DopplerCooling','doppler_cooling_amplitude_866'),
                                             ('DopplerCooling','doppler_cooling_duration'),
                                             ('DopplerCooling','doppler_cooling_include_second_397'),
                                             ]
                          }
    
    def sequence(self):
        st = self.parameters.StateReadout
        replace = {
                   'DopplerCooling.doppler_cooling_frequency_397':st.state_readout_frequency_397,
                   'DopplerCooling.doppler_cooling_amplitude_397':st.state_readout_amplitude_397,
                   'DopplerCooling.doppler_cooling_frequency_866':st.state_readout_frequency_866,
                   'DopplerCooling.doppler_cooling_amplitude_866':st.state_readout_amplitude_866,
                   'DopplerCooling.doppler_cooling_duration':st.state_readout_duration + st.camera_transfer_additional,
                   'DopplerCooling.doppler_cooling_include_second_397':st.state_readout_include_second_397,
                   }
        self.addSequence(doppler_cooling, TreeDict.fromdict(replace))
        self.addTTL('ReadoutCount', self.start, st.state_readout_duration)
        if st.use_camera_for_readout:
            self.addTTL('camera', self.start, st.camera_trigger_width)