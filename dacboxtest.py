import ok
import time
from struct import Struct
xem = ok.FrontPanel()

xem.OpenBySerial("")

xem.GetDeviceID()

#This line load a configuration file into the FPGA#

xem.ConfigureFPGA("/home/cct/LabRAD/cct/okfpgaservers/pulser2/photon.bit")

# pos 1 = \x08
# set 1 = \x02
xem.ActivateTriggerIn(0x40, 8) # reset the fifo

# voltage is in in the form:
# (3rd most )(least sign) (most sig) (2nd most)
# or
# (7 - 4) (3 - 0) (15 - 12) (11 - 8)
# pos = (15 - 11)
# set = (10 - 1)

#       3     4   1   2 
# need 0000 0010 0000 0001


xem.WriteToBlockPipeIn(0x82,2,"\x00\x00\x02\x08")
xem.WriteToBlockPipeIn(0x82,2,"\x00\x00\x00\x00")
time.sleep(2)
xem.ActivateTriggerIn(0x40,8)
xem.WriteToBlockPipeIn(0x82,2,"\xff\xff\x02\x08")
xem.WriteToBlockPipeIn(0x82,2,"\x00\x00\x00\x00")
