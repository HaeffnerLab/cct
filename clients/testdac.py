import labrad
import time

cxn = labrad.connect()
server = cxn.cctdac_pulser

voltages = range(-10,11,1)

for j in range(10):
    for v in voltages:
        server.set_individual_analog_voltages( [ (1, v) ] )
        #time.sleep(10)
    
