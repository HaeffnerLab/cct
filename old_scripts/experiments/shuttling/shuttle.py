from cct.scripts.PulseSequences.advanceDACsShuttle import advance_DACs_shuttle
from cct.scripts.PulseSequences.resetDACs import reset_DACs
from common.abstractdevices.script_scanner.scan_methods import experiment

class shuttle(experiment):
	name = 'shuttle'
	required_parameters = [
							('shuttle', 'duration'),
							('shuttle', 'position'),
							('shuttle', 'step_size'),
							('shuttle', 'loop'),
							('shuttle', 'loop_delay'),
							('shuttle', 'overshoot'),

							('advanceDACs', 'times'),
							('advanceDACs', 'pulse_length'),
						  ]

	def initialize(self, cxn, context, ident):
		print 'init'
		self.ident = ident
		self.dac_server = cxn.dac_server
		self.pulser = cxn.pulser
		print 'done init'
		# self.startPosition = self.dac_server.get_position()

	def run(self, cxn, context):
		print 'run'
		print self.parameters['shuttle.position']
		print self.parameters['shuttle.step_size']
		position = int(self.parameters['shuttle.position'])
		step_size = int(self.parameters['shuttle.step_size'])
		duration = float(self.parameters['shuttle.duration'])
		loop = bool(self.parameters['shuttle.loop'])
		loop_delay = float(self.parameters['shuttle.loop_delay'])
		overshoot = bool(self.parameters['shuttle.overshoot'])
		# shuttle_times = self.dac_server.shuttle(endPosition, step_size, duration, loop, overshoot)
		# shuttle_times = self.dac_server.get_shuttle_times()
		self.parameters['advanceDACs.times'] = self.dac_server.shuttle((position, step_size, duration, loop, loop_delay, overshoot))
		self.seq = advance_DACs_shuttle(self.parameters)
		self.doSequence()
		
		self.dac_server.set_first_voltages()
		self.seq = reset_DACs(self.parameters)
		self.doSequence()			

	def finalize(self, cxn, context):
		pass

	def doSequence(self):
		self.seq.programSequence(self.pulser)
		self.pulser.start_single()
		self.pulser.wait_sequence_done()
		self.pulser.stop_sequence()

if __name__ == '__main__':
	import labrad
	cxn = labrad.connect()
	scanner = cxn.scriptscanner
	exprt = shuttle(cxn=cxn)
	ident = scanner.register_external_launch(exprt.name)
	exprt.execute(ident)
