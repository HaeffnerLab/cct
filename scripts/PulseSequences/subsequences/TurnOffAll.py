# First try at changing for scripts
# The default state for all lasers should be OFF
# So we simply do nothing

from cct.scripts.PulseSequences.PulseSequence import PulseSequence
from labrad.units import WithUnit

class turn_off_all(PulseSequence):
    
    def sequence(self):
        pulses = self.dds_pulses
        dur = WithUnit(50, 'us')
        #dur = WithUnit(0.5, 's')
        print "working"
        #for channel in ['pump','729DP','110DP','854DP','866DP','radial']:
        pulses.append( ('729DP', self.start, dur, WithUnit(0, 'MHz'), WithUnit(0, 'dBm')))
        #self.ttl_pulses.append(('397DP', self.start, dur))
        self.end = self.start + dur
