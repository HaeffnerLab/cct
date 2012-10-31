from sequence import Sequence
import time
import numpy as np

class wireVoltage(Sequence):

    # dictionary of variable: (type, min, max, default)
    requiredVars = {
        'excitationTime':(float, 1e-3, 10.0, 1e-3),
        'bufferTime':(float, 10e-9, 10.0, 1e-3)
        }

    def defineSequence(self):

        excitationTime = self.vars['excitationTime']
        bufferTime = self.vars['bufferTime']
        
        # add_ttl_pulse has form (channel, start time, duration)
        self.pulser.add_ttl_pulse('TimeResolvedCount', 0, 25e-3 + 2*bufferTime + 2*excitationTime)
        self.pulser.add_ttl_pulse('wireVoltage', 5e-3, excitationTime) # may need to invert
        self.pulser.add_ttl_pulse('wireVoltage', 5e-3 + excitationTime + bufferTime, excitationTime)