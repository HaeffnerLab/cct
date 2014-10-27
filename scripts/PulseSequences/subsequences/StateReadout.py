from common.okfpgaservers.pulser.pulse_sequences.pulse_sequence import pulse_sequence
from cct.scripts.PulseSequences.subsequences.DopplerCooling import doppler_cooling
from treedict import TreeDict
from labrad.units import WithUnit

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
                           ('StateReadout','camera_transfer_additional')
                           ]

    required_subsequences = [doppler_cooling]
    replaced_parameters = {
                          doppler_cooling:  [('DopplerCooling','doppler_cooling_frequency_397'),
                                             ('DopplerCooling','doppler_cooling_amplitude_397'),
                                             ('DopplerCooling','doppler_cooling_frequency_866'),
                                             ('DopplerCooling','doppler_cooling_amplitude_866'),
                                             ('DopplerCooling','doppler_cooling_duration'),
                                             ('DopplerCooling', 'mode_swapping_enable'),
                                             ('ParametricCoupling', 'drive_amplitude'),
                                             ('ParametricCoupling', 'drive_frequency'),
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
                   'DopplerCooling.mode_swapping_enable':False,
                   'ParametricCoupling.drive_amplitude':WithUnit(-63.,'dBm'),
                   'ParametricCoupling.drive_frequency':WithUnit(80., 'kHz'),
                   }
        self.addSequence(doppler_cooling, TreeDict.fromdict(replace))
        self.addTTL('ReadoutCount', self.start, st.state_readout_duration)
        if st.use_camera_for_readout:
            self.addTTL('camera', self.start, st.camera_trigger_width)