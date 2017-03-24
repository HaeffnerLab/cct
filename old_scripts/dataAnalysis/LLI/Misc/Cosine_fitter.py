import labrad
import numpy as np
from matplotlib import pyplot

import lmfit

def cosine_model(params, x):
    A = params['A'].value
    tau= params['tau'].value
    freq = params['freq'].value
    phase=params['phase'].value
    output = A*np.cos(2*np.pi*x*freq+phase)*np.exp(-x/tau)
    return output
'''
define how to compare data to the function
'''
def cosine_fit(params , x, data, err):
    model = cosine_model(params, x)
    return (model - data)/err

#get access to servers
cxn = labrad.connect()
dv = cxn.data_vault


dv.cd(['','Experiments','Parity_LLI_scan_gap','2014May04','1214_49'])
dv.open(2)
data = dv.get().asarray
dv.cd(['','Experiments','Parity_LLI_scan_gap','2014May04','1254_17'])
dv.open(2)
data2 = dv.get().asarray
x = data[:,0]/1000
x2 = data2[:,0]/1000
y = np.multiply(data[:,1]*0.45/0.225,np.exp(-x/180))
y2 = np.multiply(data2[:,1]*0.45/0.225,np.exp(-x2/180))
x = x[3:]
y = y[3:]

x = np.concatenate((x,x2),axis=0)
y = np.concatenate((y,y2),axis=0)
yerr = 1/np.sqrt((1-y**2)/800)

### binner
for i in range(1,np.size(x)-1):
    print i
    y[i] = (y[i-1]+y[i]+y[i+1])/3.0
    i = i+1

figure = pyplot.figure(1)
figure.clf()



##fitter
params = lmfit.Parameters()

params.add('A', value = 0.4)
params.add('tau', value = 180)
params.add('freq', value = 0.163)
params.add('phase', value = 0.0)

result = lmfit.minimize(cosine_fit, params, args = (x, y, yerr))

fit_values  = y + result.residual

lmfit.report_errors(params)

#lmfit.report_fit(params)

#change directory
x_plot = np.linspace(x.min(),x.max(),1000)


pyplot.plot(x,y,'o',color='#00246B',zorder=3)
pyplot.plot(x_plot,cosine_model(params,x_plot),'-',linewidth=1.5,color="#A0A8B8",zorder=2)
pyplot.xlim([-1,105])
pyplot.ylim([-0.6,0.6])

pyplot.show()
