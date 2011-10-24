import serial
import binascii

ser = serial.Serial('/dev/tty.usbserial-FTFA67XY', baudrate=56000)

ser.close()
ser.open()

numPortsChanged = 1
portNum = 5
setNum = 0
codeInDec = 65535
nChanged = binascii.unhexlify(hex(numPortsChanged)[2:].zfill(2)) # Number of ports to change

comstr = nChanged
print comstr
for k in range(1,2):
    port =  binascii.unhexlify(hex(k)[2:].zfill(2)) # Which port to change
    set = binascii.unhexlify(hex(setNum)[2:].zfill(4)) # Which set of updates are we applying
    code = binascii.unhexlify(hex(int(codeInDec))[2:].zfill(4)) # What digital code to write to the port
    comstr += 'P' + port + 'I' + set + ',' + code

#comstr = nChanged + 'P' + port + 'I' + set + ',' + code + 'P' + port + 'I' + set + ',' + code
#print comstr
print ser.write(comstr)
ser.read()
ser.close()
