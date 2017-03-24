from common.okfpgaservers.pulser.pulse_sequences.pulse_sequence import pulse_sequence

class rf_pulse(pulse_sequence):
	required_parameters = [('RFPulse','rf_pulse_duration')]

	def sequence(self):
		dur = self.parameters.RFPulse.rf_pulse_duration
		self.end = self.start + dur
		self.addTTL('agilent', self.start, dur)