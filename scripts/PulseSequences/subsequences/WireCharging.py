from common.okfpgaservers.pulser.pulse_sequences.pulse_sequence import pulse_sequence

class wire_charging(pulse_sequence):
    
    
    required_parameters =  [('WireCharging','wire_charging_duration')]

    def sequence(self):
        self.end = self.start + self.parameters.WireCharging.wire_charging_duration
        self.addTTL('WireCharging', self.start, self.parameters.WireCharging.wire_charging_duration
