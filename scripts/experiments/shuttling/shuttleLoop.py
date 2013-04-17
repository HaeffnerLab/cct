from cct.scripts.PulseSequences.advanceDACsShuttleLoop import advance_DACs_shuttle
from cct.scripts.PulseSequences.resetDACs import reset_DACs
from common.abstractdevices.script_scanner.scan_methods import experiment
from labrad import types

class shuttleLoop( experiment ):
	name = 'shuttleLoop'
	required_parameters = [
							('shuttle', 'duration'),
							('shuttle', 'position'),
							('shuttle', 'delay'),							

							('advanceDACs', 'steps'),
							('advanceDACs', 'pulse_length'),
						  ]

	def initialize( self, cxn, context, ident ):
		self.ident = ident
		self.dacserver = cxn.dac_server
		self.pulser = cxn.pulser
		self.startPosition = self.dacserver.get_position()
		self.dacserver.set_first_voltages()
		self.seq = reset_DACs(self.parameters)
		self.doSequence()

	def run( self, cxn, context ):		
		endPosition = int(self.parameters['shuttle.position'])
		print 'start, end', self.startPosition, endPosition
		if endPosition == self.startPosition: return
		elif endPosition > self.startPosition: ordering = range( self.startPosition + 1, endPosition + 1) + range( self.startPosition, endPosition)[::-1]
		else: ordering = range( endPosition, self.startPosition)[::-1] + range( endPosition + 1, self.startPosition + 1)
		if len(ordering) > 126: raise Exception("Too many voltage sets!")
		for i, p in enumerate( ordering ):
			print 'pos: ', p
			should_stop = self.pause_or_stop()
			if should_stop: break
			self.dacserver.set_next_voltages( p )
		self.parameters['advanceDACs.steps'] = len(ordering/2)
		self.seq = advance_DACs_shuttle(self.parameters)
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
	exprt = shuttleLoop( cxn = cxn )
	ident = scanner.register_external_launch( exprt.name )
	exprt.execute(ident)
