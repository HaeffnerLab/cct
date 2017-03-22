from heatingrabi import HeatingRabi 
import numpy as np
import pylab as pl
import seaborn as sns

sns.set_style("white")
sns.set_style("ticks")

DO_PLOT = True

date = '2014Nov10'
hr = HeatingRabi(date, w0 = 2*np.pi*2.5e6, phi=0, nmax=10000, basepath='/home/path_to_datavault/Experiments.dir')

print "Fitting 0.2dBm"
flist = ['1934_34','1932_11','1935_44','1937_27']
tlist = np.array([0,100,50,20])
t2pi = hr.fit_t2pi(flist[0],40, do_plot=False, fit_nbar=False, nbar_guess=1000)
print t2pi
r02,dr02 = hr.get_heating_rate(flist,tlist,t2pi, do_plot=DO_PLOT, fit_t2pi=False)


print "Fitting 0.3dBm"
#flist = ['1925_41','1927_13','1928_42','1929_42']
#tlist = np.array([0,50,20,100])
flist = ['1925_41','1928_42','1929_42']
tlist = np.array([0,20,100])

t2pi = hr.fit_t2pi(flist[0],40, do_plot=False, fit_nbar=False, nbar_guess=1000)
print t2pi
r03,dr03 = hr.get_heating_rate(flist,tlist,t2pi, do_plot=DO_PLOT, fit_t2pi=False)
asd()

print "Fitting 0.4dBm"
flist = ['1918_50','1919_52','1922_56','1921_32','1922_15']
tlist = np.array([0,50,100,10,20])
t2pi = hr.fit_t2pi(flist[0],40, do_plot=False, fit_nbar=False, nbar_guess=1000)
print t2pi
r04,dr04 = hr.get_heating_rate(flist,tlist,t2pi, do_plot=DO_PLOT, fit_t2pi=False)



print "Fitting 0.5dBm"
flist = ['1938_52','1939_58','1942_21','1943_30']
tlist = np.array([0,100,20,50])
t2pi = hr.fit_t2pi(flist[0],40, do_plot=False, fit_nbar=False, nbar_guess=1000)
print t2pi
r05,dr05 = hr.get_heating_rate(flist,tlist,t2pi, do_plot=DO_PLOT, fit_t2pi=False)


print "Fitting 1.6dBm"
flist = ['1947_13','1948_09']
tlist = np.array([0,100])
t2pi = hr.fit_t2pi(flist[0],50, do_plot=False, fit_nbar=False, nbar_guess=100)
print t2pi
r16,dr16 = hr.get_heating_rate(flist,tlist,t2pi, do_plot=DO_PLOT, fit_t2pi=False)


p = [0.2, 0.3, 0.4, 0.5, 1.6]
r = [r02, r03, r04, r05, r16]
dr= [dr02, dr03, dr04, dr05, dr16]

p_hor = [0, 0.4, 1.4]
r_hor = [1.8, 11.2, 1.3]
dr_hor = [0.2, 2.6, 0.3]

pl.figure()
pl.errorbar(p,r,dr, markersize=10,fmt='rd', label='Vertical')
pl.errorbar(p_hor,r_hor,dr_hor, markersize=10,fmt='bs', label='Horizontal')
pl.ylim([-2,75])
pl.xlabel('RF drive power [dBm]')
pl.ylabel('Heating Rate [quanta/ms]')
pl.ion()
pl.savefig('20141110_heating_vs_power.pdf')
pl.legend()
