from common.okfpgaservers.pulser.pulse_sequences.pulse_sequence import pulse_sequence
from labrad.units import WithUnit
from DopplerCooling import doppler_cooling
from treedict import TreeDict

class ramsey_2ions_excitation(pulse_sequence):
    
    required_parameters = [
                          ('Ramsey_2ions','excitation_frequency'), 
                          ('Ramsey_2ions','excitation_amplitude'),
                          ('Ramsey_2ions', 'second_pulse_phase'),
                          ('Ramsey_2ions', 'ion1_excitation_duration'),
                          ('Ramsey_2ions','ion2_excitation_duration'),
                          ('Ramsey_2ions','ramsey_time'),
                          ]

    def sequence(self):
        #this hack will be not needed with the new dds parsing methods
        p = self.parameters.Ramsey_2ions
        frequency_advance_duration = WithUnit(8.0, 'us')
        ampl_off = WithUnit(-63.0, 'dBm')
        excitation_duration = p.ion1_excitation_duration + p.ion2_excitation_duration
        #detuning = WithUnit(0.0,'kHz')
        
        #self.end = self.start + frequency_advance_duration + p.rabi_excitation_duration
        self.end = self.start
        #print self.end
        ###set all frequencies but keep amplitude low first###
        self.addDDS('729', self.end, frequency_advance_duration, p.excitation_frequency, ampl_off)
        self.end = self.end + frequency_advance_duration
        
        ###pi/2 pulses###
        self.addDDS('729', self.end, excitation_duration, p.excitation_frequency, p.excitation_amplitude)
        self.addTTL('729_1', self.end, p.ion1_excitation_duration)
        self.addTTL('729_2', self.end + p.ion1_excitation_duration, p.ion2_excitation_duration)
        print 'left ion pulse 1:', p.ion1_excitation_duration
        print 'right ion pulse 1:', p.ion2_excitation_duration
        self.end = self.end + excitation_duration
        
        ### ramsey time ###
        self.end = self.end+p.ramsey_time
        print 'Ramsey_time:', p.ramsey_time
        
        ###pi/2 pulses###
        self.addDDS('729', self.end, excitation_duration, p.excitation_frequency, p.excitation_amplitude, p.second_pulse_phase)
        self.addTTL('729_1', self.end, p.ion1_excitation_duration)
        self.addTTL('729_2', self.end + p.ion1_excitation_duration, p.ion2_excitation_duration)
        self.end = self.end + excitation_duration
