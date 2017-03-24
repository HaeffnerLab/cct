from common.okfpgaservers.pulser.pulse_sequences.pulse_sequence import pulse_sequence
from labrad.units import WithUnit

class reset_DACs(pulse_sequence):
	def sequence( self ):
		self.addTTL('rst', WithUnit(0.0, 'us'), WithUnit(0.3, 'us'))
		self.addTTL('adv', WithUnit(0.1, 'us'), WithUnit(0.1, 'us'))

