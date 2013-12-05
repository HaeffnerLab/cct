from common.okfpgaservers.pulser.pulse_sequences.pulse_sequence import pulse_sequence
from RabiExcitation import rabi_excitation
from treedict import TreeDict
from labrad.units import WithUnit

class pi_pulse(pulse_sequence):
    
    required_parameters = [
        ('PiPulse', 'pi_time'),
        ('PiPulse', 'rabi_amplitude_729'),
        ('PiPulse', 'rabi_excitation_frequency'),
        ]

    required_subsequences = [rabi_excitation]

    def sequence(self):
        p = self.parameters.PiPulse
        replace = TreeDict.fromdict({
                'Excitation_729.rabi_excitation_duration': p.pi_time,
                'Excitation_729.rabi_excitation_amplitude': p.rabi_amplitude_729,
                'Excitation_729.rabi_excitation_frequency': p.rabi_excitation_frequency
                })
        self.addSequence(rabi_excitation, replace)
