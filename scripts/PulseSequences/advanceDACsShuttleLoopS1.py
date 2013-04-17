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
		times = [T/(2*math.pi)*math.acos(1 - 4.*(x)/(N)) for x in range(N/2)] + [T/(2*math.pi)*(math.pi + math.acos(1 - 4.*(x+1)/(N)) )for x in range(N/2)]
		for t in times:
			print t.value
			self.addTTL('adv', t, pl)
