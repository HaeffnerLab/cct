from common.okfpgaservers.pulser.pulse_sequences.pulse_sequence import pulse_sequence
class reset_DACs(pulse_sequence):
	required_parameters = [
							('advanceDACs', 'pulse_length'),
	]

	def sequence( self ):
		pl = self.parameters.advanceDACs.pulse_length
		self.addTTL('rst', 0*pl, 3*pl)
		self.addTTL('adv', pl, pl)

