from sequence import Sequence
channel = 0
setindex = 0
value = 0
class DACSEQ(Sequence):
    #(type, min, max, default)
#    requiredVars = {
#                         'channel':(int, 0, 31, 31),
#                         'setindex':(int, 0, 1023, 0),
#                         'value':(int, 0, 65535, 65535),
#                    }
    def defineSequence(self):
#        p = self.parameters
        channel = self.channel
        setindex = self.setindex
        value = self.value
        pulser = self.pulser
        n = 0
        dTime = 10e-6        

        start = dTime      
        duration = 2*dTime + 10e-3
        pulser.add_ttl_pulse('rst',start, duration)

        start = start + duration + dTime
        duration = 3 * dTime        
        pulser.add_ttl_pulse('dat',start, duration)

        start = start + dTime
        duration = dTime
        pulser.add_ttl_pulse('clk',start, duration)

        for i in range(5):
            start = start + 2 * dTime #4
            if channel & 0b10000:
                duration = 3 * dTime
                pulser.add_ttl_pulse('dat',start, duration)
                n=n+1

                start = start+dTime
                duration = dTime
                pulser.add_ttl_pulse('clk',start, duration)

                channel =(channel << 1) - 0b100000
            else:
                start = start+dTime
                duration = dTime
                pulser.add_ttl_pulse('clk',start, duration)

                channel =(channel << 1)

        start = start - dTime
        for i in range(10):
            start = start + 2 * dTime
            if setindex & 0b1000000000:
                duration = 3 * dTime
                pulser.add_ttl_pulse('dat',start, duration)
                n=n+1

                start = start + dTime
                duration = dTime
                pulser.add_ttl_pulse('clk',start, duration)

                setindex =(setindex << 1) - 0b10000000000
            else:
                start = start + dTime
                duration = dTime
                pulser.add_ttl_pulse('clk',start, duration)

                setindex =(setindex << 1)
                
        start = start -dTime
        for i in range(16):
            start = start + 2 * dTime
            if value & 0b1000000000000000:
                duration = 3 * dTime
                pulser.add_ttl_pulse('dat',start, duration)
                n=n+1

                start = start + dTime
                duration = dTime
                pulser.add_ttl_pulse('clk',start, duration)
                
                value =(value << 1) - 0b10000000000000000
            else:
                start = start + dTime
                duration = dTime
                pulser.add_ttl_pulse('clk',start, duration)
                
                value =(value << 1)

        start = start + dTime
        duration = dTime
        pulser.add_ttl_pulse('clk',start, duration)

        start = start + dTime
        duration = 3 * dTime        
        if n%1 == 1:
            pulser.add_ttl_pulse('dat',start, duration)

        start = start + dTime
        duration = dTime
        pulser.add_ttl_pulse('clk',start, duration)

        start = start + 2 * dTime
        duration = 12 * dTime
        pulser.add_ttl_pulse('dat',start, duration)

        start = start - dTime
        for i in range(5):
            start = statr + 2 * dTime
            duration = dTime
            pulser.add_ttl_pulse('clk',start, duration)

        start = statr + 2 * dTime
        duration = dTime ###!!!!
        pulser.add_ttl_pulse('rst',start, duration)

if __name__ == '__main__':
    import labrad
    cxn = labrad.connect()
    pulser = cxn.pulser
    seq = DACSEQ(pulser)
    pulser.new_sequence()
#    params = {
#              'channel':1.,
#              'setindex':1.,
#              'valaue':1.,
#              }
#    seq.setVariables(**params)
    seq.defineSequence()
    pulser.program_sequence()
    pulser.reset_timetags()
    pulser.start_single()
    pulser.wait_sequence_done()
    pulser.stop_sequence()
    timetags = pulser.get_timetags().asarray
    print timetags
        

        
            
        
        
        
        
        



            
        
        
            
            
        
        

        
