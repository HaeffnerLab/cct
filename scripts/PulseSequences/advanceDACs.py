from PulseSequence import PulseSequence
from labrad import types as T

class ADV_DACS(PulseSequence):
    def configuration(self):
        config = [
                  'startIndex', 'stopIndex', 'maxIndex', 'duration', 'reset'
                  ]
        return config
    
    def sequence(self):    
        n = self.p.startIndex
        dTime = T.Value(self.p.duration, 's')
        sTime = T.Value(0., 's')

        if self.p.reset:
            self.ttl_pulses.append(('rst', sTime, 3*dTime))
            self.ttl_pulses.append(('adv', sTime + dTime, dTime))
            return

        while n != self.p.stopIndex:
            if n < self.p.maxIndex:
                self.ttl_pulses.append(('adv', sTime, dTime))
                n += 1
                sTime += 2*dTime 
            else:
                self.ttl_pulses.append(('rst', sTime, 3 * dTime))
                self.ttl_pulses.append(('adv', sTime + dTime, dTime))
                n = 1
                sTime += 4*dTime                                     

class sample_parameters(object):
    
    parameters = {
              'startIndex':1,
              'stopIndex': 2,
              'maxIndex': 125,
              'duration': T.Value(10e-4, 's'),
              'reset': True
              }

if __name__ == '__main__':
    import labrad
    cxn = labrad.connect()
    params = sample_parameters.parameters
    cs = spectrum_blue_dephase(**params)
    cs.programSequence(cxn.pulser)
    cxn.pulser.start_number(100)
    cxn.pulser.wait_sequence_done()
    cxn.pulser.stop_sequence()