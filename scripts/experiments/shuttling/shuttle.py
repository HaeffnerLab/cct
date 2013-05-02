from cct.scripts.PulseSequences.advanceDACsShuttle import advance_DACs_shuttle
from cct.scripts.PulseSequences.resetDACs import reset_DACs
from common.abstractdevices.script_scanner.scan_methods import experiment

class shuttle( experiment ):
	name = 'shuttle'
	required_parameters = [
							('shuttle', 'duration'),
							('shuttle', 'position'),
							('shuttle', 'step_size'),

							('advanceDACs', 'steps'),
							('advanceDACs', 'pulse_length'),
						  ]

	def initialize( self, cxn, context, ident ):
		self.ident = ident
		self.dacserver = cxn.dac_server
		self.pulser = cxn.pulser
		self.startPosition = self.dacserver.get_position()

	def run( self, cxn, context ):		
		endPosition = int(self.parameters['shuttle.position'])
		stepSize = int(self.parameters['shuttle.step_size'])		
		if endPosition == self.startPosition: return
		elif endPosition > self.startPosition: 
			endPosition -= (endPosition - self.startPosition)%stepSize
			ordering = range( self.startPosition + stepSize, endPosition + stepSize, stepSize)
		else: 
			endPosition += (endPosition - self.startPosition)%stepSize
			ordering = range( endPosition, self.startPosition, stepSize)[::-1]
		if len(ordering) > 126: raise Exception("Too many voltage sets!")
		for i, p in enumerate( ordering ):
			should_stop = self.pause_or_stop()
			if should_stop: break
			self.dacserver.set_next_voltages( p )
		self.parameters['advanceDACs.steps'] = len(ordering)
		self.seq = advance_DACs_shuttle(self.parameters)
		self.doSequence()
		
		self.dacserver.set_first_voltages()
		self.seq = reset_DACs(self.parameters)
		self.doSequence()			

	def finalize( self, cxn, context ):
		pass

	def doSequence( self ):
		self.seq.programSequence( self.pulser )
		self.pulser.start_single()
		self.pulser.wait_sequence_done()
		self.pulser.stop_sequence()

if __name__ == '__main__':
	import labrad
	cxn = labrad.connect()
	scanner = cxn.scriptscanner
	exprt = shuttle( cxn = cxn )
	ident = scanner.register_external_launch( exprt.name )
	exprt.execute(ident)
