from sequence import Sequence
import time
import numpy as np

class DopplerRecool(Sequence):

    # dictionary of variable: (type, min, max, default)
    requiredVars = {
        'recordTime':(float, 10e-9, 1, 100e-3),
        'darkTime':(float, 1e-3, 5, 1e-3)
        }

    def defineSequence(self):

        recordTime = self.vars['recordTime']
        darkTime = self.vars['darkTime']
        
        # add_ttl_pulse has form (channel, start time, duration)
        self.pulser.add_ttl_pulse('866sw', 0.0, darkTime) # may need to invert
        self.pulser.add_ttl_pulse('TimeResolvedCount', darkTime, recordTime)
