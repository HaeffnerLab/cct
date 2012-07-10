from visa import instrument
import scipy
import scipy.io
from numpy import *
import numpy as np
from scipy.io import loadmat
import serial
import time
import binascii
import matplotlib.pyplot as plt
import datetime

now = datetime.datetime.now()



keithley = instrument("USB0::0x05E6::0x2100::1243106::INSTR")
#ser=serial.Serial(port='\\.\COM3', baudrate=9600, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=1)
ser = serial.Serial("COM7",baudrate=56000)

ser.close()
ser.open()


#outVoltKeithley = scipy.zeros((2,65536))



# startNr and maxNr: available digital representations: 0 :: 2**16 - 1
# go through these representations in steps of size 100
startNr = 0
maxNr = 65535
step = 100
nElectrodes = 42

# A vector of all the digital codes we're going to check
vecsize=int(round((maxNr-startNr)/step))

print vecsize
print startNr + step * vecsize
outVoltKeithley = scipy.zeros((2,vecsize))

# NOT SURE WHAT THIS DOES YET
# just some non-exact values to avoid overloads...
calVector = scipy.ones((nElectrodes,3), float)
for i in range(nElectrodes):
        calVector[i,0] = -1.49918e1
        calVector[i,1] = 0.000425043
        calVector[i,2] = -8.69927e-13
        
#keithley.write("SENS:AVER:STAT ON")
#keithley.write("SENS:AVER:TCON REP")
#keithley.write("SENS:AVER:COUN 10")

for k in range(6,19+1):

        for j in range(1,vecsize):

                i = startNr + step * j 
        
                nr = '%d' % i
                nrWrite = hex(i)[2:]
                print i

		# Just make sure nrWrite is 4 hex characters (this can be done in an easier way)
		# nrWrite = hex(i)[2:].zfill(4)

                if len(nrWrite) == 3: nrWrite = '0' + nrWrite
                if len(nrWrite) == 2: nrWrite = '00' + nrWrite
                if len(nrWrite) == 1: nrWrite = '000' + nrWrite

                #print nrWrite
                nrWrite = binascii.unhexlify(nrWrite)

                formSetNr = hex(1)[2:]

                if len(formSetNr) == 1: formSetNr = "000" + formSetNr
                if len(formSetNr) == 2: formSetNr = "00" + formSetNr
                if len(formSetNr) == 3: formSetNr = "0" + formSetNr
                formSetNr = binascii.unhexlify(formSetNr)

                formPortNr = hex(k)[2:]	
                if len(formPortNr) == 1: formPortNr = "0" + formPortNr				
                formPortNr = binascii.unhexlify(formPortNr)
	
                # concetenate string
                writeString =  "P" + formPortNr + "I" + formSetNr + "," + nrWrite

                formnumberPorts = hex(2)[2:]	
                if len(formnumberPorts) == 1: formnumberPorts = "0" + formnumberPorts				
                formnumberPorts = binascii.unhexlify(formnumberPorts)
                
                finalWriteString = formnumberPorts + writeString + writeString
       	
                ser.write(finalWriteString)
                
                time.sleep(0.1)
                #keithley.write("SENS:VOLT:DC:NPLC 10")
                #outVoltRead = keithley.ask_for_values("MEAS:VOLT:DC? 100,0.0001")
                #keithley.write("*RST;*CLS")
                outVoltRead = keithley.ask_for_values("MEAS:VOLT:DC?")
                #outVoltRead = keithley.ask_for_values("MEAS:VOLT:DC?")
                
                
                
                outVoltKeithley[0,j] = nr 
                outVoltKeithley[1,j] = outVoltRead[0] 

                print outVoltRead[0]
        
        print outVoltKeithley[0,:]
        print outVoltKeithley[1,:]

        z = np.polyfit(outVoltKeithley[0,500:vecsize],outVoltKeithley[1,500:vecsize], 2)
        print z
        yp = np.poly1d(z)
        xp = np.linspace(10, maxNr, 10)


        plt.plot(outVoltKeithley[0,:],outVoltKeithley[1,:],'ro')
        plt.plot(outVoltKeithley[0,:],outVoltKeithley[1,:], 'ro',xp,yp(xp),'-')
        plt.ylabel('some numbers')
        plt.show()

        calVector[k-1,0] = z[2]
        calVector[k-1,1] = z[1]
        calVector[k-1,2] = z[0]

        saveString1 = "dac_amp_cal_data_%d.txt" % (k)
        savetxt(saveString1, [outVoltKeithley[0,:],outVoltKeithley[1,:]])

print calVector

ser.close()
keithley.write("system:local")
keithley.close()
#saveString1 = "dac_amp_cal_data_%d-%d-%d-%dh%d.txt" % (now.year,now.month,now.day,now.hour,now.minute)
#saveString2 = "polyfit_%d-%d-%d-%dh%d.txt" % (now.year,now.month,now.day,now.hour,now.minute)
#savetxt(saveString1, [outVoltKeithley[0,:],outVoltKeithley[1,:]])
#savetxt(saveString2, z)

savetxt("dac_amp_cal_vector.txt",calVector)
