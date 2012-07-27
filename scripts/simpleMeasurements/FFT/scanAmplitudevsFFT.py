from FFT import measureFFT
import numpy as np
import labrad
import time

cxn = labrad.connect()
dv = cxn.data_vault
ds = cxn.cctdac
#rs = cxn.rohdeschwarz_server
#rs.select_device('lattice-pc GPIB Bus - USB0::0x0AAD::0x0054::102549')

amplMin = -1
amplMax = 1
amplStep = .2
recordTime = 0.5 #seconds
average = 4
freqSpan = 300.0 #Hz 
freqOffset = -889.0 #Hz, the offset between the counter clock and the rf synthesizer clock
#setting up FFT
fft = measureFFT(cxn, recordTime, average, freqSpan, freqOffset, savePlot = False)
#saving
dv.cd(['','QuickMeasurements','FFT'],True)
name = dv.new('FFT',[('Amplitude', 'V/m')], [('FFTPeak','Arb','Arb')] )
dv.add_parameter('plotLive',True)
print 'Saving {}'.format(name)

amplitudes = np.arange(amplMin, amplMax + amplStep, amplStep)

for Ex in amplitudes:
    ds.set_multipole_voltages([('Ex', Ex)])
    micromotion = fft.getPeakArea(ptsAround = 3)
    dv.add(Ex, micromotion)
rs.amplitude(initampl)
