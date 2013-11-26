from cct.scripts.PulseSequences.advanceDACsShuttle import advance_DACs_shuttle
from cct.scripts.PulseSequences.resetDACs import reset_DACs
from common.abstractdevices.script_scanner.scan_methods import experiment
from labrad import types
# import matplotlib
# from matplotlib import pyplot as plt

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
		# matplotlib.use('Qt4agg')
		self.volts = {}

	def run( self, cxn, context ):		
		endPosition = int(self.parameters['shuttle.position'])
		stepSize = int(self.parameters['shuttle.step_size'])		
		print 'start, end', self.startPosition, endPosition
		if endPosition == self.startPosition: return
		elif endPosition > self.startPosition: 
			endPosition -= (endPosition - self.startPosition)%stepSize
			ordering = range( self.startPosition + stepSize, endPosition + stepSize, stepSize)
		else: 
			endPosition += (endPosition - self.startPosition)%stepSize
			ordering = range( endPosition, self.startPosition, stepSize)[::-1]
		# if len(ordering) > 126: raise Exception("Too many voltage sets!")
		for i, p in enumerate( ordering ):
			print 'pos: ', p
			should_stop = self.pause_or_stop()
			if should_stop: break
			self.dacserver.set_next_voltages( p )
			av = self.dacserver.get_analog_voltages()
			for e, v in av:
				try: self.volts[e].append(v)
				except: self.volts[e] = [v]
		self.parameters['advanceDACs.steps'] = len(ordering)
		self.seq = advance_DACs_shuttle(self.parameters)
		# self.doSequence()
		
		self.dacserver.set_first_voltages()
		self.seq = reset_DACs(self.parameters)
		# self.doSequence()			

	def finalize( self, cxn, context ):
		print self.volts.keys()
		print [self.volts[k] for k in self.volts.keys()]

	def doSequence( self ):
		self.seq.programSequence( self.pulser )
		self.pulser.start_single()
		self.pulser.wait_sequence_done()
		self.pulser.stop_sequence()

if __name__ == '__main__':
	# matplotlib.use('Qt4agg')
	import labrad
	cxn = labrad.connect()
	scanner = cxn.scriptscanner
	exprt = shuttle( cxn = cxn )
	ident = scanner.register_external_launch( exprt.name )
	exprt.execute(ident)
