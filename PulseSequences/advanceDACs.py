from sequence import Sequence
class ADV_DAC(Sequence):
    #(type, min, max, default)
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
        startIndex = p.startIndex
        stopIndex = p.stopIndex
        maxIndex = p.maxIndex
        dTime = p.duration              
        sTime = 0
        n = startIndex
        
        if p.reset: 
            pulser.add_ttl_pulse('rst', sTime, 3 * dTime)
            pulser.add_ttl_pulse('adv', sTime + dTime, dTime)
            return
        
        while n != stopIndex:
            if n < maxIndex:
                pulser.add_ttl_pulse('adv', sTime, dTime)
                n += 1
                sTime += 2*dTime
            elif n == maxIndex:
                pulser.add_ttl_pulse('rst', sTime, 3 * dTime)
                pulser.add_ttl_pulse('adv', sTime + dTime, dTime)
                n = 1
                sTime += 4*dTime

if __name__ == '__main__':
    import labrad
    cxn = labrad.connect()
    pulser = cxn.pulser
    seq = ADV_DAC(pulser)
    pulser.new_sequence()
    params = {
              'startIndex':1,
              'stopIndex':100,
              'maxIndex':1000,
              }
    seq.setVariables(**params)
    seq.defineSequence()
    pulser.program_sequence()
    pulser.start_single()
    pulser.wait_sequence_done()
    pulser.stop_sequence()