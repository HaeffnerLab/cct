from common.okfpgaservers.pulser.pulse_sequences.pulse_sequence import pulse_sequence
    
class parametric_coupling(pulse_sequence):

	required_parameters = [
                  ('ParametricCoupling','parametric_coupling_duration'),
                  ]

	def sequence(self):
		p = self.parameters.ParametricCoupling
		dur = p.parametric_coupling_duration

		print dur

		self.end = self.start + dur
		self.addTTL('parametric_modulation', self.start, dur)