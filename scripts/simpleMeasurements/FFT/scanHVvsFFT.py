from FFT import measureFFT
import numpy as np
import labrad
import time

cxn = labrad.connect()
dv = cxn.data_vault

recordTime = 0.5 #seconds
average = 4
freqSpan = 20.0 #Hz 
freqOffset = -889 #Hz, the offset between the counter clock and the rf synthesizer clock
#setting up FFT
fft = measureFFT(cxn, recordTime, average, freqSpan, freqOffset, savePlot = False)
#saving
dv.cd(['','QuickMeasurements','FFT', 'Compensation'],True)
name = dv.new('FFT',[('number', 'n')], [('FFTPeak','Arb','Arb')] )
dv.add_parameter('plotLive',True)
print 'Saving {}'.format(name)

for j in range(100):
    time.sleep(1)
    micromotion = fft.getPeakArea(ptsAround = 3)
    dv.add(j, micromotion)
	print micromotion