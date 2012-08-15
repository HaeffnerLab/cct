from sequence import Sequence

class HeatSeq(Sequnce):
    #dictionary of variables: (type, min, max, default)
    requiredVars = {
                         'initial_cooling':(float, 10e-9, 5.0, 100e-3), 

                         }
                         
                         
if __name__ == '__main__':
    import labrad
    cxn = labrad.connect()
    pulser = cxn.pulser
    pulser.new_sequence()
    seq = LatentHeatGlobalHeat(pulser)
    #sequence parameters
    params = {
              'initial_cooling': 500e-3,

              }
    seq.setVariables(**params)
    seq.defineSequence()
    pulser.program_sequence()
    pulser.reset_timetags()
    pulser.start_single()
    pulser.wait_sequence_done()
    pulser.stop_sequence()
    timetags = pulser.get_timetags().asarray
    print 'got {} timetags'.format(timetags.size)
