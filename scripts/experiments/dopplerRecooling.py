# heating rate measurement by Doppler recooling

import sys
sys.path.append('/home/cct/LabRAD/cct/scripts')
sys.path.append('/home/cct/LabRAD/cct/scripts/PulseSequences')

import labrad
from labrad import types
import numpy
import time

from fly_processing import Binner
from PulseSequences.dopplerRecooling import DopplerRecool
from scriptLibrary import dvParameters

class Bunch:
    def __init__(self, **kwds):
        self.__dict__.update(kwds)
    
    def __setitem__(self, key, val):
        self.__dict__[key] = val
    
    def toDict(self):
        return self.__dict__


class DopplerRecooling():
    experimentName = 'Heating_rate_doppler'

    def __init__(self, seqParams, exprmtParams):
        self.cxn = labrad.connect()
        self.cxnlab = labrad.connect('192.168.169.49') # labwide network
        
        self.dv = self.cxn.data_vault
        self.pulser = self.cxn.pulser
        self.seqP = Bunch(**seqParams)
        self.expP = Bunch(**exprtParams)
        self.Binner = None

    def initialize(self):
        self.dirappend = time.strftime("%Y%m%d_%H%M_%S",time.localtime())
        self.topdirectory = time.strftime("%Y%m%d",time.localtime())
        self.setupLogic()
        self.programPulser()
        
        totalBinningTime = self.seqP.recordTime + self.seqP.recoolTime + self.seqP.darkTime
        self.Binner = Binner(totalBinningTime, self.expP.binTime)

    def setupLogic(self):
        self.pulser.switch_auto('397sw', True) # High TTL corresponds to light ON

    def programPulser(self):
        seq = DopplerRecool(self.pulser)
        self.pulser.new_sequence()
        seq.setVariables(**self.seqP.toDict())
        seq.defineSequence()
        self.pulser.program_sequence()
        self.seqP['recordTime'] = seq.parameters.recordTime
        self.seqP['darkTime'] = seq.parameters.darkTime
        self.seqP['recoolTime'] = seq.parameters.recoolTime

    def run(self):
        self.initialize()
        self.sequence()
        self.finalize()
        print "done"

    def sequence(self):

        sP = self.seqP
        xP = self.expP

        self.dv.cd(['','Experiments', self.experimentName, self.topdirectory, self.dirappend], True)
        self.dv.new('binned_timetags',[('Time', 'sec')],[('PMT counts','Arb','Arb')] )
        self.dv.add_parameter('Window',['Binned Fluorescence'])
        self.dv.add_parameter('plotLive', True)        

        for iteration in range(xP.iterations):
            self.pulser.reset_timetags()
            self.pulser.start_single()
            self.pulser.wait_sequence_done()
            self.pulser.stop_sequence()

            timetags = self.pulser.get_timetags().asarray
            #print len(timetags)
            print len(timetags)
            self.Binner.add(timetags)

        # Recording data

        binX, binY = self.Binner.getBinned()
        data = numpy.vstack((binX,binY)).transpose()
        self.dv.add(data)
        print sum(binY)

        measureList = ['cavity397', 'cavity866', 'multiplexer397', 'multiplexer866', 'pulser']
        measureDict = dvParameters.measureParameters(self.cxn, self.cxnlab, measureList)

        dvParameters.saveParameters(self.dv, measureDict)
        dvParameters.saveParameters(self.dv, sP.toDict())
        dvParameters.saveParameters(self.dv, xP.toDict())


    def finalize(self):
        self.pulser.switch_auto('397sw')

    def __del__(self):
        self.cxn.disconnect()

if __name__ == '__main__':
    params = {
        'recordTime':100e-3,
        'darkTime':1.0,
        'recoolTime':100e-3
        }

    exprtParams = {
        'iterations':100,
        'binTime': 50.0*10**-6
        }

    exprt = DopplerRecooling(params, exprtParams)
    exprt.run()
