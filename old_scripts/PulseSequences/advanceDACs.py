from common.okfpgaservers.pulser.pulse_sequences.pulse_sequence import pulse_sequence
class advance_DACs(pulse_sequence):
	required_parameters = [
							('advanceDACs', 'pulse_length'),
							('advanceDACs', 'steps'),
	]

	def sequence( self ):
		pl = self.parameters.advanceDACs.pulse_length
		for step in range(self.parameters.advanceDACs.steps):
			self.addTTL('adv', 2*step*pl, pl)

