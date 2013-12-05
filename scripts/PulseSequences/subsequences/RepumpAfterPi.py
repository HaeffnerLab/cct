from common.okfpgaservers.pulser.pulse_sequences.pulse_sequence import pulse_sequence
from RepumpD import repump_d
from OpticalPumping import optical_pumping

class repump_after_pi_pulse(pulse_sequence):
	required_parameters = [
    	('RepumpAfterPiPulse','repump_d_duration'), 
        ('RepumpAfterPiPulse','repump_d_frequency_854'), 
        ('RepumpAfterPiPulse','repump_d_amplitude_854'),
        ('RepumpAfterPiPulse', 'optical_pumping_duration')
        ]
    required_subsequences = [repump_d, optical_pumping ]
    def sequence(self):

