import labrad
cxn = labrad.connect()

svrs = [ 'GPIB Bus', 'GPIB Device Manager', 'Keithley 2100 DMM']

for s in svrs:
    cxn.node_cctmain.start(s)

cxn.gpib_device_manager.dump_info()
