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
                  ('ParametricCoupling','pulse_shaping'),
                  ]

	def sequence(self):
		p = self.parameters.ParametricCoupling
		coupling_time = self.parameters['ParametricCoupling.parametric_coupling_duration']
		freq = self.parameters['ParametricCoupling.drive_frequency']
		shape_time = 20.0
		if p.pulse_shaping:
			coupling_time = coupling_time['us']
			N_points = p.N_points
			exp_corr = 1/.42 #Correction to keep the area constant
			#black_up_time = np.linspace(0,shape_time,int(N_points/2.0))
			#black_down_time = np.linspace(0,shape_time,int(N_points/2.0)) + coupling_time
			#wait_time = np.linspace(0,(coupling_time['us']-shape_time),Npoints) + shape_time # - swap_time/2*exp_corr
			#time = np.hstack([black_up_time, black_down_time])
			#x_black = np.linspace(0,1,int(N_points) )

			time = np.linspace(0,coupling_time * exp_corr,N_points)# - swap_time/2*exp_corr
			delta_t = time[1] - time[0]
			T = (1/freq)['us']
			t0 = coupling_time * exp_corr
			alph = .16
			a = [(1-alph)/2.0, 1/2., alph/2.]

			#y_blackman = a[0] - a[1] * np.cos(2*np.pi*x_black) +  a[2] * np.cos(4*np.pi*x_black) # voltage ratio to max voltage
			y_blackman = a[0] - a[1] * np.cos(2*np.pi*time/t0) +  a[2] * np.cos(4*np.pi*time/t0) # voltage ratio to max voltage
			start_times = []
			amplitude = WithUnit(-63, 'dBm')
			dur = WithUnit(8.0, 'us')
			self.addDDS('parametric_coupling', self.start, dur, freq, amplitude, p.parametric_coupling_phase)
			dur = WithUnit(delta_t, 'us')
			
			for (t, y) in zip(time, y_blackman):
				start_time = WithUnit(t, 'us') + self.start + WithUnit(8,'us')
				if y < 1e-5:
					amplitude = WithUnit(-62, 'dBm')
				else:
					amplitude = WithUnit(20*np.log10(y), 'dBm') + p.drive_amplitude
					#amplitude = p.drive_amplitude
				if amplitude < WithUnit(-63., 'dBm'):
					amplitude = WithUnit(-63, 'dBm')
				self.addDDS('parametric_coupling', start_time, dur, freq, amplitude, p.parametric_coupling_phase)
			
			#amplitude = p.drive_amplitude
			#t = shape_time 
			#start_time = WithUnit(t + 8, 'us') + self.start + dur
			#dur = WithUnit(coupling_time - shape_time , 'us') -dur
			#self.addDDS('parametric_coupling', start_time, dur, freq, amplitude, p.parametric_coupling_phase)
						
			total_duration = WithUnit(time[-1], 'us') + dur + WithUnit(8,'us')
			self.end = self.start + total_duration
		else:
			self.addDDS('parametric_coupling', self.start, p.parametric_coupling_duration, p.drive_frequency, p.drive_amplitude, p.parametric_coupling_phase )
			self.end = self.start + p.parametric_coupling_duration
