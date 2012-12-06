import time
import numpy as np
import matplotlib.pyplot as plt
import labrad.types as T
import labrad
cxn = labrad.connect()
ds = cxn.cctdac_serial
sa = cxn.advantest_server
reg = cxn.registry
freqs = []
# digVoltages = range(17000, 65000, 600)
digVoltages = range(29600, 65000, 600)
ds.set_individual_digital_voltages([(3, digVoltages[0])])
for i in digVoltages:
	ds.set_individual_digital_voltages([(3, i)])
	time.sleep(.1)
	dat = sa.get_peak_info()
	freq = dat[0]
	freqs.append(freq)
fit = np.polyfit(freqs, digVoltages, 3)
c0 = T.Value(fit[3], '')
c1 = T.Value(fit[2]*1e6, '1/MHz')
c2 = T.Value(fit[1]*1e12,'1/MHz^2')
c3 = T.Value(fit[0]*1e18, '1/MHz^3')
print 'c0', c0
print 'c1', c1
print 'c2', c2
reg.cd(['', 'Servers', 'VCO', '397DP', 'calibration'], True)
reg.set('c0', c0)
reg.set('c1', c1)
reg.set('c2', c2)
reg.set('c3', c3)
plt.plot(freqs, digVoltages)
plt.show()

