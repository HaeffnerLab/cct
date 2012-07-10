#@author: Dylan Gorman

"""

Manual control for optical shutters.


"""

from labrad.server import import LabradServer, setting, Signal
from twisted.internet.defer import Deferred, returnValue, inlineCallbacks
from twisted.internet.task import LoopingCall
import time

SIGNALID = 331499

class ManualShutterControl( LabradServer ):
    
    @inlineCallbacks
    def initServer(self):
        
        self.pulser = yield self.client.pulser
        
        self.channels = ['BluePI', '866']
        
    @inlineCallbacks
    def setChannelTrue(self):
        
        self.pulser.switch