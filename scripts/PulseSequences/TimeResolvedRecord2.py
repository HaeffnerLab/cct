from scripts.PulseSequences.PulseSequence import PulseSequence
import time
import numpy as np
from labrad import types as T

class TimeResolved(PulseSequence):
    def configuration(self):
        config = [
            'recordTime'
            ]
        return config

    def sequence(self):
        
        self.ttl_pulses.append(('TimeResolvedCount', self.start, self.p.recordTime))

class sample_parameters(object):

    parameters = {
#        'centerFreq':T.Value(100,'Hz'),
        'recordTime':T.Value(2,'s'),
#        'freqOffset':T.Value(0,'Hz'),
#        'freqSpan':T.Value(20,'Hz'),
#        'numToAverage':4
        }

if __name__ == '__main__':
    import labrad
    cxn = labrad.connect()
    pulser = cxn.pulser

    params = sample_parameters.parameters

    seq = TimeResolved(**params)

    seq.programSequence(pulser)

    pulser.reset_timetags()
    pulser.start_number(1)
    pulser.wait_sequence_done()
    pulser.stop_sequence()

    print 'completed', pulser.repeatitions_completed()
    timetags = pulser.get_timetags().asarray
    print timetags[0:249]
    counts = []
    print 'measured {0} timetags'.format(timetags.size)
