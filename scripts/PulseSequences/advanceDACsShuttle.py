from common.okfpgaservers.pulser.pulse_sequences.pulse_sequence import pulse_sequence
from labrad.units import WithUnit

class advance_DACs_shuttle(pulse_sequence):
	required_parameters = [
							('advanceDACs', 'pulse_length'),
							('advanceDACs', 'times'),
	]

	def sequence( self ):
		pl = self.parameters.advanceDACs.pulse_length
		times = self.parameters.advanceDACs.times
		for t in times:
			self.addTTL('adv', WithUnit(t, 's'), pl)
