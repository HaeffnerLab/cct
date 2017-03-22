import labrad
import numpy
import time

cxn = labrad.connect()
tps = cxn.cctmain_tps_server()

while(1):
    optstr=raw_input('taking data on pressing return, enter string to be added to filename:\n')
    writearray=tps.getcurve().asarray
    filename='F:/Documents and Settings/gandalf/Desktop/data_resonator/curve_osci_'+time.strftime("%d%m%Y_%H%M_")+optstr+'.csv'
    numpy.savetxt(filename,writearray)
    #time.sleep(60)
