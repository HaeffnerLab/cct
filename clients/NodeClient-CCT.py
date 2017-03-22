# import labrad
# import numpy as np
# import time

# nodeDict = {'node_cctmain':
# 					['Serial Server','Data Vault','Pulser', 'DAC Server', 'NormalPMTFlow', 'Piezo Server', 'SD Tracker', 'ParameterVault', 'ScriptScanner'],
# 					# ['Serial Server','Data Vault','Pulser', 'NormalPMTFlow','CCTDAC', 'Piezo Server', 'Semaphore']
# 		}


# #connect to LabRAD
# errors = False
# try:
# 	cxn = labrad.connect()
# except:
# 	print 'Please start LabRAD Manager'
# 	errors = True
# else:
# 	nodes = nodeDict.keys()
# 	if not len(nodes):
# 		print "No Nodes Running"
# 		errors = True
# 	for node in nodeDict.keys():
# 		#make sure all node servers are up
# 		if not node in cxn.servers:'{} is not running'.format(node)
# 		else:
# 			print '\nWorking on {} \n '.format(node)
# 			cxn.servers[node].refresh_servers()
# 			#if node server is up, start all possible servers on it that are not already running
# 			running_servers = np.array(cxn.servers[node].running_servers().asarray)
# 			for server in nodeDict[node]:
# 				if server in running_servers: 
# 					print server + ' is already running'
# 				else:
# 					print 'starting ' + server
# 					try:
# 						cxn.servers[node].start(server)
# 					except Exception as e:
# 						print 'ERROR with ' + server
# 						errors = True
	
# if errors:
# 	time.sleep(10)

import labrad
import numpy as np
import time

##nodeDict = {'node_cctmain':
##					['Data Vault','Serial Server','Pulser','NormalPMTFlow','DAC Server', 'GPIB Bus',
##					'GPIB Device Manager','Agilent Server', 'RohdeSchwarz Server','SD Tracker', 
##					'ScriptScanner','ParameterVault']					
##		}
nodeDict = {'node_bender':
					['Data Vault','Pulser','NormalPMTFlow','DAC Server', 'SD Tracker', 
					'ScriptScanner','ParameterVault']					
		}
#connect to LabRAD
errors = False
try:
        cxn = labrad.connect()
except Exception:
	print 'Please start LabRAD Manager'
else:
	nodes = nodeDict.keys()
	if not len(nodes):
		print "No Nodes Running"
	for node in nodeDict.keys():
		#make sure all node servers are up
		if not node in cxn.servers: print '{} is not running'.format(node)
		else:
			print '\nWorking on {} \n '.format(node)
			cxn.servers[node].refresh_servers()
			#if node server is up, start all possible servers on it that are not already running
			running_servers = np.asarray(cxn.servers[node].running_servers())
			for server in nodeDict[node]:
				if server in running_servers: 
					print server + ' is already running'
				else:
					print 'starting ' + server
					try:
						cxn.servers[node].start(server)
					except Exception as e:
						print 'ERROR with ' + server
			time.sleep(2)
print 'DONE'	
