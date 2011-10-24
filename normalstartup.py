import labrad
cxn = labrad.connect()
node = cxn.node_cctmain
node.start('Serial Server')
node.start('CCTDAC')
#node.start('GPIB Bus')
#node.start('GPIB Device Manager')
node.start('Data Vault')
node.start('Paul Box')
node.start('Trigger')
node.start('Normal PMT Counts FPGA')
node.start('Normal PMT Flow')

#cxn.node_cctmain.start('RS Server trapdrive sideband')
