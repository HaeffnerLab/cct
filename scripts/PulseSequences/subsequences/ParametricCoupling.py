from common.okfpgaservers.pulser.pulse_sequences.pulse_sequence import pulse_sequence
import numpy as np
from labrad.units import WithUnit
    
class parametric_coupling(pulse_sequence):

	required_parameters = [
                  ('ParametricCoupling','parametric_coupling_duration'),
                  ('ParametricCoupling','drive_frequency'),
                  ('ParametricCoupling','N_points'),
                  ('ParametricCoupling','drive_amplitude'),
                  ('ParametricCoupling','parametric_coupling_phase'),
                  ]

	def sequence(self):
		p = self.parameters.ParametricCoupling
		coupling_time = self.parameters['ParametricCoupling.parametric_coupling_duration']
		freq = self.parameters['ParametricCoupling.drive_frequency']
		coupling_time = coupling_time['us']
		N_points = p.N_points
		exp_corr = 1/.42 #Correction to keep the area constant
		time = np.linspace(0,coupling_time * exp_corr,N_points)# - swap_time/2*exp_corr
		delta_t = time[1] - time[0]
		T = (1/freq)['us']
		print T
		phase_offset = WithUnit( (time/T)*360, 'deg')
		t0 = coupling_time * exp_corr
		alph = .16
		a = [(1-alph)/2.0, 1/2., alph/2.]
		y_blackman = a[0] - a[1] * np.cos(2*np.pi*time/t0) +  a[2] * np.cos(4*np.pi*time/t0) # voltage ratio to max voltage
		start_times = []
		dur = WithUnit(delta_t, 'us')
		for (t, y) in zip(time, y_blackman):
			start_time = WithUnit(t, 'us') + start
			amplitude = WithUnit(20*np.log10(y), 'dBm') + P_max
			self.addDDS(dds, start_time, dur, freq, amplitude, phase + phase_offset)
		total_duration = WithUnit(time[-1], 'us') + dur
		self.end = self.start + total_duration