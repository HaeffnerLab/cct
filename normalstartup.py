import labrad
cxn = labrad.connect()
node = cxn.node_cctmain
node.start('Data Vault')
#node.start('NormalPMTFlow')
#node.start('CCTDAC Pulser')
node.start('Serial Server')
node.start('CCTDAC')
node.start('Piezo Server')
#node.start('GPIB Bus')
#node.start('GPIB Device Manager')
#node.start('Pulser')
#cxn.node_cctmain.start('RS Server trapdrive sideband')
