'''
A hack to accomplish pulse shaping.

'''

import numpy as np
from labrad.units import WithUnit

class pulse_shaper():

	def add_shaped_DDS(self, dds, start, coupling_time, freq, P_max, Npoints, phase = 0, shape_time=10.):
		'''
		y_blackman is the window if the output is given in volts. in order to change the ouput voltage by
		a factor of c, the output power needs to increase by 20*log(c).

		Also we need to keep track of the phase during this.
		'''
        exp_corr = 1/.42 #Correction to keep the area constant
        x_black = np.linspace(0,1,int(Npoints) )
        black_up_time = np.linspace(0,shape_time,int(Npoints/2.0))
        black_down_time = np.linspace(0,shape_time,int(Npoints/2.0)) + coupling_time['us']
        #wait_time = np.linspace(0,(coupling_time['us']-shape_time),Npoints) + shape_time # - swap_time/2*exp_corr
        time = np.hstack([black_up_time, black_down_time])
        delta_t = time[1] - time[0]
        T = (1/freq)['us']
    	phase_offset = WithUnit( (time/T)*360, 'deg')
    	t0 = coupling_time['us'] * exp_corr

    	alph = .16
    	a = [(1-alph)/2.0, 1/2., alph/2.]
    	y_blackman = a[0] - a[1] * np.cos(2*np.pi*x_black) +  a[2] * np.cos(4*np.pi*x_black) # voltage ratio to max voltage
    	start_times = []
    	dur = WithUnit(delta_t, 'us')
    	for (t, y) in zip(time, y_blackman):
        	start_time = WithUnit(t, 'us') + start
        	amplitude = WithUnit(20*np.log10(y), 'dBm') + P_max
    		self.addDDS(dds, start_time, dur, freq, amplitude, phase + phase_offset)
        amplitude = P_max
        t = shape_time
        start_time = WithUnit(t, 'us') + start
        duration = coupling_time - shape_time
        self.addDDS(dds, start_time, dur, freq, amplitude, phase + phase_offset)
        return WithUnit(time[-1] + delta_t,'us') # total duration of the shaped pulse
