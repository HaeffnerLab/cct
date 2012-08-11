import ok
import time
from struct import Struct
xem = ok.FrontPanel()

xem.OpenBySerial("")

xem.GetDeviceID()

#This line load a configuration file into the FPGA#

xem.ConfigureFPGA("/home/cct/LabRAD/cct/okfpgaservers/pulser/photon.bit")

# Set the mode to normal
print xem.SetWireInValue(0x00,0x00,0x01)
print xem.UpdateWireIns()

print "reading from primary"
xem.SetWireInValue(0x00,0x40,0xf0)
xem.UpdateWireIns()
xem.UpdateWireOuts()
print xem.GetWireOutValue(0x21)

print "reading from secondary"
xem.SetWireInValue(0x00, 0xa0, 0xf0)
xem.UpdateWireIns()
xem.UpdateWireOuts()
print xem.GetWireOutValue(0x21)
