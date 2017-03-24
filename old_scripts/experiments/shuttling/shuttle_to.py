from cct.scripts.PulseSequences.advanceDACsShuttle_to import advance_DACs_shuttle
from cct.scripts.PulseSequences.resetDACs import reset_DACs
from common.abstractdevices.script_scanner.scan_methods import experiment

class shuttle(experiment):
	name = 'shuttle'
	required_parameters = [
							# ('shuttle', 'duration'),
							# ('shuttle', 'position'),
							# ('shuttle', 'step_size'),
							# ('shuttle', 'loop'),
							# ('shuttle', 'loop_delay'),
							# ('shuttle', 'overshoot'),

							('advanceDACs', 'times'),
							('advanceDACs', 'pulse_length'),
						  ]

	def initialize(self, cxn, context, ident):
		print 'init'
		self.ident = ident
		self.dac_server = cxn.dac_server_dev
		self.pulser = cxn.pulser
		# self.parameter_vault = cxn.parametervault
		print 'done init'
		# self.startPosition = self.dac_server.get_position()

	def run(self, cxn, context):
		print 'run'
		# pos = yield self.parameters['shuttle.position']
		# print pos
		# print self.parameters['shuttle.step_size']

		# issues with deffered instances from parameter vault on starting experiment from DACServer. Ask pv directly.

		# self.dac_server.write_shuttle_voltages()
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
