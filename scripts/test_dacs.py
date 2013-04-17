# configuration
setVolts = [-2.46, 5.83]
compVolts = [None, None]
allowedDeviation = .1
iterations = 1000
channel = '02'

# script
from time import sleep
import labrad
from random import random
cxn = labrad.connect()
cxncam = labrad.connect('192.168.169.30')
dacserver = cxn.dac_server
dmmserver = cxncam.keithley_2100_dmm
dmmserver.select_device('cct_camera GPIB Bus - USB0::0x05E6::0x2100::1243106')

print "Running DAC test..."
dacserver.set_individual_analog_voltages([(channel, setVolts[0])]*2)
sleep(.3)
compVolts[0] = dmmserver.get_dc_volts()

dacserver.set_individual_analog_voltages([(channel, setVolts[1])]*2)
sleep(.3)
compVolts[1] = dmmserver.get_dc_volts()

print compVolts
numErrors = 0
for i in range(iterations):
	print "iteration: {}".format(i)
	for n, v in enumerate(setVolts):
		for l in range(10): dacserver.set_individual_analog_voltages([(channel, random())]*2)
		dacserver.set_individual_analog_voltages([(channel, v)]*2)
		sleep(.3)
		measuredVoltage = dmmserver.get_dc_volts()
		# print measuredVoltage
		# print abs(compVolts[n] - measuredVoltage)
		if abs(compVolts[n] - measuredVoltage) > allowedDeviation:
			numErrors += 1
			print "error: {}".format(numErrors)

PE = numErrors*50./iterations
print 'Test complete, error rate: {}%'.format(PE)
