from common.okfpgaservers.pulser.pulse_sequences.pulse_sequence import pulse_sequence
    
class pulsed_heating(pulse_sequence):

	required_parameters = [
                  ('PulsedHeating','pulsed_heating_duration'),
                  ('PulsedHeating','pulsed_heating_amplitude_397'),
                  ('PulsedHeating','pulsed_heating_frequency_397'),
                  ('DopplerCooling','doppler_cooling_frequency_866'), 
                  ('DopplerCooling','doppler_cooling_amplitude_866')
                  ]

	def sequence(self):
		ph = self.parameters.PulsedHeating
		dc = self.parameters.DopplerCooling
		dur = ph.pulsed_heating_duration

		self.end = self.start + dur
		self.addTTL('397mod', self.start, dur)
		#self.addDDS ('397',self.start, dur, ph.pulsed_heating_frequency_397, ph.pulsed_heating_amplitude_397)
		self.addDDS ('866',self.start, dur, dc.doppler_cooling_frequency_866, dc.doppler_cooling_amplitude_866)
