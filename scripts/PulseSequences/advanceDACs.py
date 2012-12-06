from sequence import Sequence
import labrad.types as T
class ADV_DAC(Sequence):
    requiredVars = {
                         'startIndex':(int, 1, 1000, 1),
                         'stopIndex':(int, 1, 1000, 2),
                         'maxIndex':(int, 100, 1000, 1000),
                         'duration':(float, 10e-8, 10e-2, 10e-2),
                         'reset':(int, 0, 1, 0)
                    }
    def defineSequence(self):
        pulser = self.pulser
        p = self.parameters
        n = p.startIndex
        dTime = T.Value(p.duration, 's')
        sTime = T.Value(0., 's')

        if p.reset:
            pulser.add_ttl_pulse('rst', sTime, 3 * dTime)
            pulser.add_ttl_pulse('adv', sTime + dTime, dTime)
            return
        
        while n != p.stopIndex:
            if n < p.maxIndex:
                pulser.add_ttl_pulse('adv', sTime, dTime)
                n += 1
                sTime += 2*dTime
            else:
                pulser.add_ttl_pulse('rst', sTime, 3 * dTime)
                pulser.add_ttl_pulse('adv', sTime + dTime, dTime)
                n = 1
                sTime += 4*dTime