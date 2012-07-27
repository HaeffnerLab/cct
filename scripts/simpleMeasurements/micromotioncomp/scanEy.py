from FFT import measureFFT
import numpy as np
import labrad
import datetime

now = datetime.datetime.now()
date = now.strftime("%Y%m%d")

cxn = labrad.connect()
dv = cxn.data_vault
ds = cxn.cctdac
#rs = cxn.rohdeschwarz_server
#rs.select_device('lattice-pc GPIB Bus - USB0::0x0AAD::0x0054::102549')

amplMin = -.4
amplMax = -.3
amplStep = .01
recordTime = 0.5 #seconds
average = 6
freqSpan = 100.0 #Hz 
freqOffset = -920.0 #Hz, the offset between the counter clock and the rf synthesizer clock
#setting up FFT
fft = measureFFT(cxn, recordTime, average, freqSpan, freqOffset, savePlot = False)
#saving

dv.cd(['', date, 'QuickMeasurements','FFT'],True)
name = dv.new('FFT',[('Amplitude', 'V/m')], [('FFTPeak','Arb','Arb')] )
dv.add_parameter('plotLive',True)
print 'Saving {}'.format(name)

amplitudes = np.arange(amplMin, amplMax + amplStep, amplStep)
Ex = 0.19
Ez = 0
U1 = -.22
U2 = 4.5
U3 = .22
U4 = 0
U5 = 0

for Ey in amplitudes:
    ds.set_multipole_voltages([('Ex', Ex), ('Ey', Ey), ('Ez', Ez), ('U1', U1), ('U2', U2), ('U3', U3), ('U4', U4), ('U5', U5)])
    micromotion = fft.getPeakArea(ptsAround = 3)
    dv.add(Ey, micromotion)
