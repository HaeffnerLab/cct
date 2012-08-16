import labrad
import numpy
import time

cxn = labrad.connect()
tps = cxn.tektronixtds_server()
tps.select_device()

while(1):
    optstr=raw_input('taking data on pressing return, enter string to be added to filename:\n')
    answer=tps.getcurve()
    outstring = ''
    for x in range(len(answer)):
        outstring = outstring + str(( (answer[x])[0] ).value)
        outstring = outstring + ' '
        outstring = outstring + str(( (answer[x])[1] ).value )
        outstring = outstring + '\n'
    filename='data_resonator/curve_osci_'+time.strftime("%d%m%Y_%H%M_")+optstr+'.csv'
    #numpy.savetxt(filename,outstring)
    f = open(filename, 'w')
    f.write(outstring)
    f.close

    #time.sleep(60)
