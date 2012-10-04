import labrad
cxn = labrad.connect()
node = cxn.node_cctmain
node.start('Data Vault')
node.start('Serial Server')
node.start('CCTDAC')
node.start('Piezo Server')
#node.start('Pulser')
#node.start('NormalPMTFlow')
#node.start('CCTDAC Pulser')
