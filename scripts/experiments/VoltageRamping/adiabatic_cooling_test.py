from space_time.scripts.PulseSequences.advanceDACsShuttle import advance_DACs_shuttle
from space_time.scripts.PulseSequences.resetDACs import reset_DACs
from common.abstractdevices.script_scanner.scan_methods import experiment
from space_time.scripts.experiments.Experiments729.excitations import excitation_729
from space_time.scripts.experiments.Experiments729.excitations import excitation_729_with_multipole_ramp
from space_time.scripts.scriptLibrary.common_methods_729 import common_methods_729 as cm
from space_time.scripts.scriptLibrary import dvParameters

#from space_time.scripts.experiments.Crystallization.crystallization import crystallization

import time
import labrad
from labrad.units import WithUnit
import numpy as np

class adiabatic_cooling_test(experiment):
	name = 'adiabatic_cooling_test'
	required_parameters = [
							('Ramp', 'duration'),
							('Ramp', 'initial_field'),
							('Ramp', 'final_field'),
							('Ramp', 'total_steps'),
							('Ramp', 'multipole'),

							('advanceDACs', 'times'),
							('advanceDACs', 'pulse_length'),
	
	   					   ('Spectrum','custom'),
						   ('Spectrum','normal'),
						   ('Spectrum','fine'),
						   ('Spectrum','ultimate'),
						   
						   ('Spectrum','line_selection'),
						   ('Spectrum','manual_amplitude_729'),
						   ('Spectrum','manual_excitation_time'),
						   ('Spectrum','manual_scan'),
						   ('Spectrum','scan_selection'),
						   ('Spectrum','sensitivity_selection'),
						   ('Spectrum','sideband_selection'),

						   ('TrapFrequencies','axial_frequency'),
						   ('TrapFrequencies','radial_frequency_1'),
						   ('TrapFrequencies','radial_frequency_2'),
						   ('TrapFrequencies','rf_drive_frequency'),
						   
						   ]
	
	spectrum_optional_parmeters = [
						  ('Spectrum', 'window_name')
						  ]
####	
	@classmethod
	def all_required_parameters(cls):
		parameters = set(cls.required_parameters)
		parameters = parameters.union(set(excitation_729.all_required_parameters()))
		parameters = list(parameters)
		#removing parameters we'll be overwriting, and they do not need to be loaded
#		parameters.remove(('Excitation_729','rabi_excitation_amplitude'))
#		parameters.remove(('Excitation_729','rabi_excitation_duration'))
#		parameters.remove(('Excitation_729','rabi_excitation_frequency'))
		return parameters	
###	
	def initialize(self, cxn, context, ident):
		self.ident = ident  #
		self.dac_ser
		ver = cxn.dac_server
		self.pulser = cxn.pulser
		
		self.excite = self.make_experiment(excitation_729_with_multipole_ramp)
		self.excite.initialize(cxn, context, ident)
		self.scan = []
		self.amplitude = None
		self.duration = None
		self.drift_tracker = cxn.sd_tracker
		self.dv = cxn.data_vault
		self.spectrum_save_context = cxn.context()

	def setup_sequence_parameters(self):
		sp = self.parameters.Spectrum
		if sp.scan_selection == 'manual':
			minim,maxim,steps = sp.manual_scan
			duration = sp.manual_excitation_time
			amplitude = sp.manual_amplitude_729
		elif sp.scan_selection == 'auto':
			center_frequency = cm.frequency_from_line_selection(sp.scan_selection, None , sp.line_selection, self.drift_tracker)
			center_frequency = cm.add_sidebands(center_frequency, sp.sideband_selection, self.parameters.TrapFrequencies)
			span, resolution, duration, amplitude = sp[sp.sensitivity_selection]
			minim = center_frequency - span / 2.0
			maxim = center_frequency + span / 2.0
			steps = int(span / resolution )
		else:
			raise Exception("Incorrect Spectrum Scan Type")
		#making the scan
		self.parameters['Excitation_729.rabi_excitation_duration'] = duration
		self.parameters['Excitation_729.rabi_excitation_amplitude'] = amplitude
		minim = minim['MHz']; maxim = maxim['MHz']
		self.scan = np.linspace(minim,maxim, steps)
		self.scan = [WithUnit(pt, 'MHz') for pt in self.scan]
		
		## here
		#import IPython
		#IPython.embed()
		
		
	def setup_data_vault(self):
		localtime = time.localtime()
		datasetNameAppend = time.strftime("%Y%b%d_%H%M_%S",localtime)
		dirappend = [ time.strftime("%Y%b%d",localtime) ,time.strftime("%H%M_%S", localtime)]
		directory = ['','Experiments']
		directory.extend([self.name])
		directory.extend(dirappend)
		self.dv.cd(directory ,True, context = self.spectrum_save_context)
		output_size = self.excite.output_size
		dependants = [('Excitation','Ion {}'.format(ion),'Probability') for ion in range(output_size)]
		self.dv.new('Spectrum {}'.format(datasetNameAppend),[('Excitation', 'us')], dependants , context = self.spectrum_save_context)
		window_name = self.parameters.get('Spectrum.window_name', ['Spectrum'])
		self.dv.add_parameter('Window', window_name, context = self.spectrum_save_context)
		self.dv.add_parameter('plotLive', True, context = self.spectrum_save_context)


	def run(self, cxn, context):
		self.setup_data_vault()
		self.setup_sequence_parameters()
		duration = float(self.parameters['Ramp.duration'])
		total_steps = int(self.parameters['Ramp.total_steps'])
		initial_field = float(self.parameters['Ramp.initial_field'])
		final_field = float(self.parameters['Ramp.final_field'])
		multipole = str(self.parameters['Ramp.multipole'])
		
		#program in DAC voltage ramp
		self.dac_server.ramp_multipole(multipole, initial_field, final_field, total_steps)
		time_interval = duration/float(total_steps) #in us
		time_interval = time_interval * 10**-6
		self.parameters['advanceDACs.times'] = [i*time_interval for i in range(0,total_steps+1)]
		
		for i,freq in enumerate(self.scan):
			should_stop = self.pause_or_stop()
			if should_stop: break
						
			# start: run sequence directly
			self.parameters['Excitation_729.rabi_excitation_frequency'] = freq
			self.excite.set_parameters(self.parameters)
			excitation, readouts = self.excite.run(cxn, context)
			
			#self.dac_server.set_first_voltages()
			
			# end: run sequence directly
			
			if excitation is None: break
			submission = [freq['MHz']]
			submission.extend(excitation)
			self.dv.add(submission, context = self.spectrum_save_context)
			self.update_progress(i)

	def finalize(self, cxn, context):
		self.excite.finalize(cxn, context)
		#self.save_parameters(self.dv, cxn, self.cxnlab, self.spectrum_save_context)

	def update_progress(self, iteration):
		progress = self.min_progress + (self.max_progress - self.min_progress) * float(iteration + 1.0) / len(self.scan)
		self.sc.script_set_progress(self.ident,  progress)

	def save_parameters(self, dv, cxn, cxnlab, context):
		measuredDict = dvParameters.measureParameters(cxn, cxnlab)
		dvParameters.saveParameters(dv, measuredDict, context)
		dvParameters.saveParameters(dv, dict(self.parameters), context)  

if __name__ == '__main__':
	cxn = labrad.connect()
	scanner = cxn.scriptscanner
	exprt = adiabatic_cooling_test(cxn=cxn)
	ident = scanner.register_external_launch(exprt.name)
	exprt.execute(ident)