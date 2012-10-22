from sequence import Sequence
import time
import numpy as np

class wireVoltage(Sequence):

    # dictionary of variable: (type, min, max, default)
    requiredVars = {
        'excitationTime':(float, 1e-3, 1, 1e-3),
        'bufferTime':(float, 10e-9, 1.0, 1e-3)
        }

    def defineSequence(self):

        excitationTime = self.vars['excitationTime']
        bufferTime = self.vars['bufferTime']
        
        # add_ttl_pulse has form (channel, start time, duration)
        self.pulser.add_ttl_pulse('TimeResolvedCount', 0, bufferTime + excitationTime)
        self.pulser.add_ttl_pulse('wireVoltage', bufferTime, excitationTime) # may need to invert
