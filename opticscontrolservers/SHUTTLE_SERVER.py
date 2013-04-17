'''
### BEGIN NODE INFO
[info]
name = Shuttle Server
version = 1.0
description =
instancename = Shuttle Server

[startup]
cmdline = %PYTHON% %FILE%
timeout = 20

[shutdown]
message = 987654321
timeout = 20

### END NODE INFO
'''
from labrad.server import LabradServer, setting, Signal, inlineCallbacks
from twisted.internet import reactor
from twisted.internet.defer import returnValue
from scipy import interpolate
from scipy.interpolate import UnivariateSpline as UniSpline
from time import *
from numpy import *
import sys
from cct.scripts.PulseSequences.advanceDACs import ADV_DACS
from DacConfiguration import hardwareConfiguration as hc

SERVERNAME = 'Shuttle Server'
SIGNALID = 270837

class shuttleServer( LabradServer ):
	name = SERVERNAME
	serNode = 'cctmain'
	onNewUpdate = Signal(SIGNALID, 'signal: ports updated', 's')
	registryPath = ['', 'Servers', SERVERNAME]
	@inlineCallbacks
	def initServer( self ):
		from labrad.wrappers import connectAsync
		cxn = yield connectAsync()
		self.pulser = cxn.pulser
		self.dacserver = cxn.cctdac
		self.registry = self.client.registry
		self.ionInfo = {}     
		self.listeners = set()

	@setting( 0, "Shuttle Ion", position = 'i: position to move to', duration = 'v: total travel time')
	def shuttleIon(self, c, position, duration):
		yield self.dacserver.set_first_voltages()
		yield self.advDACs(reset = 1)
		startPosition = yield self.dacserver.getPosition()
		if position > self.startPosition: ordering = range(self.positionIndex, position)
		else: ordering = range(position, self.positionIndex)[::-1]
		for i in ordering:
			yield self.dacserver.set_next_voltages(c, i)
		yield self.advDACs(steps = len(ordering), duration = duration)
                
    def advDACs(self, steps = 1, duration = 1e-5, reset = 0):        
        """Pulse Sequence"""
        params = {
        		  'steps': steps,
                  'duration': duration,
                  'reset': reset
                 }
        seq = ADV_DACS(**params)
        seq.programSequence(self.pulser) 
        self.pulser.start_number(1)
        self.pulser.wait_sequence_done()
        self.pulser.stop_sequence()
        if reset: self.nextDACIndex = 1
        self.DACIndex = self.nextDACIndex
