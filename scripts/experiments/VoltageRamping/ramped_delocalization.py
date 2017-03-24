#from space_time.scripts.PulseSequences.advanceDACsShuttle import advance_DACs_shuttle
#from space_time.scripts.PulseSequences.resetDACs import reset_DACs
from common.abstractdevices.script_scanner.scan_methods import experiment
from space_time.scripts.experiments.Experiments729.excitations import excitation_729
#from space_time.scripts.scriptLibrary.common_methods_729 import common_methods_729 as cm
from space_time.scripts.scriptLibrary import dvParameters
from space_time.scripts.experiments.Camera.ion_ring_state_detector import ion_ring_state_detector
from common.okfpgaservers.pulser.pulse_sequences.pulse_sequence import pulse_sequence
from space_time.scripts.PulseSequences.delocalization_test import delocalization_test
import cv2

#from space_time.scripts.experiments.Crystallization.crystallization import crystallization

import labrad
from labrad.units import WithUnit
import numpy as np

class ramped_delocalization(experiment):
	name = 'ramped delocalization'
	required_parameters = [
							('Ramp', 'duration'),
							('Ramp', 'initial_field'),
							('Ramp', 'final_field'),
							('Ramp', 'total_steps'),
							('Ramp', 'multipole'),

							('advanceDACs', 'times'),
							('advanceDACs', 'pulse_length'),

						   ('TrapFrequencies','axial_frequency'),
						   ('TrapFrequencies','radial_frequency_1'),
						   ('TrapFrequencies','radial_frequency_2'),
						   ('TrapFrequencies','rf_drive_frequency'),
						   
						   ('IonsOnCamera','ring_center_x'),
						   ('IonsOnCamera','ring_center_y'),
						   ('IonsOnCamera','threshold'),
						   ('IonsOnCamera','ring_center_x'),
						   
						   ('IonsOnCamera','vertical_min'),
						   ('IonsOnCamera','vertical_max'),
						   ('IonsOnCamera','vertical_bin'),
						   ('IonsOnCamera','horizontal_min'),
						   ('IonsOnCamera','horizontal_max'),
						   ('IonsOnCamera','horizontal_bin'),
						   
						   ('StateReadout','state_readout_duration'),
						   ('StateReadout','repeat_each_measurement'),
						   ('StateReadout','state_readout_amplitude_397'),
						   ('StateReadout','state_readout_frequency_397'),
						   ('StateReadout','state_readout_amplitude_866'),
						   ('StateReadout','state_readout_frequency_866'),
						   ('StateReadout','camera_trigger_width'),
						   ('StateReadout','camera_transfer_additional'),
						   
						   ('DelocalizationTest','freq_729'),
						   ('DelocalizationTest','tolerance'),
						   
						   ('Heating', 'background_heating_time'),
						   ('OpticalPumping','optical_pumping_enable'), 
						   ('SidebandCooling','sideband_cooling_enable')
						   
						   ]
	
	required_subsequences = [delocalization_test]

	@classmethod
	def all_required_parameters(cls):
		parameters = set(cls.required_parameters)
		parameters = parameters.union(set(excitation_729.all_required_parameters()))
		parameters = list(parameters)
		return parameters	

	def initialize(self, cxn, context, ident):
		p = self.parameters.IonsOnCamera
		self.fitter = ion_ring_state_detector()
		self.ident = ident
		self.camera = cxn.andor_server
		self.dac_server = cxn.dac_server
		self.pulser = cxn.pulser
		
		self.image_region = image_region = [
							 int(p.horizontal_bin),
							 int(p.vertical_bin),
							 int(p.horizontal_min),
							 int(p.horizontal_max),
							 int(p.vertical_min),
							 int(p.vertical_max),
							 ]
		self.camera.abort_acquisition()
		self.initial_exposure = self.camera.get_exposure_time()
		self.camera.set_exposure_time(self.parameters.StateReadout.state_readout_duration)
		self.initial_region = self.camera.get_image_region()
		self.initial_mode = self.camera.get_acquisition_mode()
		self.initial_trigger_mode = self.camera.get_trigger_mode()		
		
		self.camera.set_acquisition_mode('Kinetics')
		self.camera.set_image_region(*image_region)
		self.camera.set_trigger_mode('External')
		#self.camera.set_trigger_mode
		self.exposures = 2
		self.camera.set_number_kinetics(self.exposures)
		#generate the pulse sequence
		self.parameters.StateReadout.use_camera_for_readout = True
		self.start_time = WithUnit(20, 'ms') #do nothing in the beginning to let the camera transfer each image
		#self.sequence = delocalization_test(self.parameters, start = start_time)
		#self.sequence = pulse_sequence(self.parameters, start = start_time)
		#self.sequence.addSequence(delocalization_test)		

		self.scan = []
		self.amplitude = None
		self.duration = None
		self.drift_tracker = cxn.sd_tracker
		self.dv = cxn.data_vault
		self.spectrum_save_context = cxn.context()
		
	def run(self, cxn, context):
		self.camera.start_acquisition()		
		
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

		# start: run sequence directly
		self.parameters['Excitation_729.rabi_excitation_frequency'] = self.parameters['DelocalizationTest.freq_729']
		self.sequence = delocalization_test(self.parameters, start = self.start_time)
		self.sequence.programSequence(self.pulser)
		self.pulser.start_number(self.exposures)
		self.pulser.wait_sequence_done()
		self.pulser.stop_sequence()
		
		proceed = self.camera.wait_for_kinetic()
		if not proceed:
			self.camera.abort_acquisition()
			self.finalize(cxn, context)
			raise Exception ("Did not get all kinetic images from camera")
		images = self.camera.get_acquired_data(self.exposures).asarray
		
		x_pixels = int( (self.image_region[3] - self.image_region[2] + 1.) / (self.image_region[0]) )
		y_pixels = int(self.image_region[5] - self.image_region[4] + 1.) / (self.image_region[1])
		images = np.reshape(images, (self.exposures, y_pixels, x_pixels))
					
		initial_config = self.find_configuration(images[0])		
		final_config = self.find_configuration(images[1])
		
		#test1 = cv2.imread('/home/space-time/Desktop/test1.jpg')  ##load image somehow	
		#test2 = cv2.imread('/home/space-time/Desktop/test2.jpg')	
		#initial_config = self.find_configuration(test1)		
		#final_config = self.find_configuration(test2)		
		
		delocalized = self.fitter.compare_configs(initial_config,final_config,self.parameters['DelocalizationTest.tolerance'])
		
		print delocalized

	def find_configuration(self,image):
		p = self.parameters.IonsOnCamera
		radial_positions = self.fitter.find_radial_positions(image,(p.ring_center_x,p.ring_center_y),p.threshold)
		return radial_positions

	def finalize(self, cxn, context):
		pass
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
	exprt = ramped_delocalization(cxn=cxn)
	ident = scanner.register_external_launch(exprt.name)
	exprt.execute(ident)