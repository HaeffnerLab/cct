from cct.scripts.PulseSequences.resetDACs import reset_DACs
from common.abstractdevices.script_scanner.scan_methods import experiment
from labrad import types

class resetDACs( experiment ):
	name = 'resetDACs'
	required_parameters = [
							('advanceDACs', 'pulse_length'),
						  ]

	def initialize( self, cxn, context, ident ):
		self.ident = ident
		self.dacserver = cxn.dac_server
		self.pulser = cxn.pulser

	def run( self, cxn, context ):		
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
	exprt = resetDACs( cxn = cxn )
	ident = scanner.register_external_launch( exprt.name )
	exprt.execute(ident)
