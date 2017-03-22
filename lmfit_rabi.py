from lmfit import Parameters, report_fit, minimize
from rabi_flop_fitter import *
import numpy as np
import pylab as pl
import scipy.constants as const

k = 2 * np.pi / 729.14e-9
w0 = 2*np.pi*1e6
eta0 = k * np.sqrt(const.hbar/(2*40*const.m_p*w0))


class rabifit:
    def __init__(self, nmax=10000):
        self.params = Parameters()
        self.params.add('nbar', value=.1, vary=False, min=0.)
        self.params.add('delta', value=0, min=-0.05, 
                        max=.1, vary=False)
        self.params.add('time_2pi', value=20, vary=True, min=0.1)
        self.params.add('coh_time', value=2000, vary=False, min=0)
        self.params.add('eta', value=0.06, vary=False, min=0)
        self.eta = 0.06
        self.sideband = 0
        self.result = None
        self.nmax = nmax

    def residual(self, params, x, data=None, eps=None):
        # unpack parameters:
        #  extract .value attribute for each parameter
        nbar = params['nbar'].value
        delta = params['delta'].value
        time_2pi = params['time_2pi'].value
        coh_time  = params['coh_time'].value
        eta  = params['eta'].value
        te = rabi_flop_time_evolution(self.sideband ,eta, nmax=self.nmax)
        model = te.compute_evolution_decay_thermal(abs(coh_time), nbar = nbar, delta = delta,
                                                   time_2pi = time_2pi, t = x)
        if data is None:
            return model
        if eps is None:
            return (model - data)
        return (model - data)/eps    

    def minimize(self, data):
        self.result = minimize(self.residual,self.params, args = (data[:,0], data[:,1], data[:,2]+.01))

if __name__ == '__main__':
    import simple_analysis.get_data as gd
    do = gd.ReadData('2014Jun24',experiment='RabiFlopping')
    dat = do.get_data('1946_08')
    f = rabifit()
    t = np.linspace(0,200,200)
    f.minimize(dat)
    time_2pi = f.result.params['time_2pi'].value
    y = f.residual(f.result.params, t)
    f1, (a1,a2,a3) = pl.subplots(3)   
    a1.plot(dat[:,0],dat[:,1])
    a1.plot(t,y)

    # Second Carrier flop
    t = np.linspace(0,800,200)
    f = rabifit()
    f.sideband = 0
    f.params['coh_time'].vary = True
    f.params['time_2pi'].value = 190
    dat = do.get_data('2000_22')
    f.minimize(dat)
    coh_time = f.params['coh_time'].value
    a2.plot(dat[:,0],dat[:,1])
    y = f.residual(f.result.params, t)
    a2.plot(t,y)

    # BSB flop
    t = np.linspace(0,800,200)
    f = rabifit()
    f.sideband = 1
    f.params['coh_time'].vary = False
    f.params['coh_time'].value= coh_time 
    f.params['time_2pi'].vary = False
    f.params['time_2pi'].value = time_2pi
    f.params['eta'].vary = True
    dat = do.get_data('2023_24')
    f.minimize(dat)
    coh_time = f.params['coh_time'].value
    a3.plot(dat[:,0],dat[:,1])
    y = f.residual(f.result.params, t)
    a3.plot(t,y)
    f.result.params['coh_time'].value = coh_time * 1e3
    y = f.residual(f.result.params, t)
    a3.plot(t,y)
    pl.show()
    phi = np.arctan(f.result.params['eta'].value/eta0) * 180/np.pi
    
