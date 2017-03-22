from __future__ import division
from heatingrabi import HeatingRabi 
import numpy as np
import pylab as pl
import seaborn as sns
sns.set_context('poster')

DO_PLOT = True

date = '2014Nov10'
hr = HeatingRabi(date, w0 = 2*np.pi*2.5e6, phi=np.pi/4, nmax=3000)

print "Fitting 0dBm"

flist = ['2212_20','2213_55','2216_43']
tlist = np.array([0,50,100])
t2pi = hr.fit_t2pi(flist[0],10, do_plot=True, fit_nbar=False)
print t2pi
r0,dr0 = hr.get_heating_rate(flist,tlist,t2pi, do_plot=DO_PLOT, fit_t2pi=False)

print "Fitting 0.4dBm"

#flist = ['2229_55','2232_22','2233_30','2235_00']
#tlist = np.array([0,50,20,100])
flist = ['2229_55','2232_22','2233_30']
tlist = np.array([0,50,20])

t2pi = hr.fit_t2pi(flist[0],10, do_plot=True, fit_nbar=False)

print t2pi
r04,dr04 = hr.get_heating_rate(flist,tlist,t2pi, do_plot=DO_PLOT, fit_t2pi=False)


print "Fitting 1.4dBm"

#flist = ['2229_55','2232_22','2233_30','2235_00']
#tlist = np.array([0,50,20,100])
flist = ['2302_19','2303_57','2307_07']
tlist = np.array([0,50,100])

t2pi = hr.fit_t2pi(flist[0],10, do_plot=True, fit_nbar=False)

print t2pi
r14,dr14 = hr.get_heating_rate(flist,tlist,t2pi, do_plot=DO_PLOT, fit_t2pi=False)

fcoil = 2.643e6
Q=1e3
gamma = fcoil/Q
x = np.linspace(2.45e6,2.85e6,1000)
y =  3 * gamma**2 / ((x-fcoil)**2+(gamma/2)**2) 
dfradial = 0.03
freq = np.array([2.49e6,2.62e6,2.8e6])

dfreq = np.array([dfradial,dfradial,dfradial])
pl.figure()
pl.errorbar(freq/1e6, [r0,r04,r14],[dr0,dr04,dr14],dfreq,fmt='rs')
pl.plot(x/1e6,y)
pl.xlabel('RF amplitude [MHz]')
pl.ylabel('Heating rate [quanta/ms]')
pl.show()


