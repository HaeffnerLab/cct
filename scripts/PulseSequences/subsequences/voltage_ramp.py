from common.okfpgaservers.pulser.pulse_sequences.pulse_sequence import pulse_sequence
from labrad.units import WithUnit 

class ramp_voltage(pulse_sequence):
    
    required_parameters = [ ('Ramp', 'duration'),
                            ('Ramp', 'initial_field'),
                            ('Ramp', 'final_field'),
                            ('Ramp', 'total_steps'),
                            ('Ramp', 'multipole'),

                            ('advanceDACs', 'times'),
                            ('advanceDACs', 'pulse_length')
    ]

    def sequence(self):
        pl = self.parameters.advanceDACs.pulse_length
        times = self.parameters.advanceDACs.times
        for t in times:
            self.addTTL('adv', self.start+WithUnit(t, 's'), pl)
        self.end = self.start + WithUnit(times[-1], 's')+pl

        