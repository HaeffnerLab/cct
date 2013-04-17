from common.okfpgaservers.pulser.pulse_sequences.pulse_sequence import pulse_sequence
import math
class advance_DACs_shuttle(pulse_sequence):
	required_parameters = [
							('advanceDACs', 'pulse_length'),
							('advanceDACs', 'steps'),

							('shuttle', 'duration'),
	]

	def sequence( self ):
		pl = self.parameters.advanceDACs.pulse_length
		T = self.parameters.shuttle.duration
		N = self.parameters.advanceDACs.steps
		if N ==1: times = 0.
                else: times = [2*T/math.pi*math.asin(math.sqrt(n/(N-1.))) for n in range(N)]
		for t in times:
			print t.value
			self.addTTL('adv', t, pl)
