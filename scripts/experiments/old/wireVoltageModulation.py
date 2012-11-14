# wire voltage modulation

#import sys
#sys.path.append('/home/cct/LabRAD/cct/scripts')
#sys.path.append('/home/cct/LabRAD/cct/scripts/PulseSequences')

import labrad
from labrad import types
import numpy
import time
import datetime

from fly_processing import Binner
from scripts.PulseSequences.wireVoltageModulation import wireVoltage
from scripts.scriptLibrary import dvParameters

class Bunch:
    def __init__(self, **kwds):
        self.__dict__.update(kwds)
    
    def __setitem__(self, key, val):
        self.__dict__[key] = val
    
    def toDict(self):
        return self.__dict__


class WireVoltageModulation():
    experimentName = 'Wire_Voltage_Modulation'

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
        
        totalBinningTime = 2*self.seqP.bufferTime + self.seqP.excitationTime
        self.Binner = Binner(totalBinningTime, self.expP.binTime)

    def setupLogic(self):
        self.pulser.switch_auto('wireVoltage', True)

    def programPulser(self):
        seq = wireVoltage(self.pulser)
        self.pulser.new_sequence()
        seq.setVariables(**self.seqP.toDict())
        seq.defineSequence()
        self.pulser.program_sequence()
        self.seqP['excitationTime'] = seq.parameters.excitationTime
        self.seqP['bufferTime'] = seq.parameters.bufferTime

    def run(self):
        self.initialize()
        self.sequence()
        self.finalize()
        print "done"

    def sequence(self):

        sP = self.seqP
        xP = self.expP
        
        now = datetime.datetime.now()
        date = now.strftime("%Y%m%d")
        ti = now.strftime('%H%M%S')
        print ti
        timetag_context = self.dv.context()
        self.dv.cd(['',date, self.experimentName,'binned'], True)
        self.dv.cd(['',date, self.experimentName, 'timetags'], True, context = timetag_context)
        #self.dv.new('binned_timetags',[('Time', 'sec')],[('PMT counts','Arb','Arb')] )
        self.dv.new(ti,[('Time', 'sec')], [('Iteration', 'Arb','Arb')] , context = timetag_context )

        timetags = []
        numUpdates = xP.iterations
        self.pulser.reset_timetags()
        for n in range(numUpdates):
            print n
            for iteration in range(xP.iterations / numUpdates):
                self.pulser.start_single()
                self.pulser.wait_sequence_done()
                self.pulser.stop_sequence()

            timetags.extend(self.pulser.get_timetags().asarray)
            self.pulser.reset_timetags()
    
        timetag_raw = numpy.vstack( ( numpy.ones(len(timetags)),timetags ) ).transpose()
        self.dv.add( timetag_raw, context=timetag_context )
        self.Binner.add(timetags, xP.iterations)
            
        self.dv.new(ti,[('Time', 'sec')],[('PMT counts','Arb','Arb')] )
        self.dv.add_parameter('Window',['Binned Fluorescence'])
        self.dv.add_parameter('plotLive', True)
        binX, binY = self.Binner.getBinned()
        data = numpy.vstack((binX,binY)).transpose()
        self.dv.add(data)
            
        measureList = ['cavity397', 'cavity866', 'multiplexer397', 'multiplexer866', 'pulser']
        measureDict = dvParameters.measureParameters(self.cxn, self.cxnlab, measureList)

        dvParameters.saveParameters(self.dv, measureDict)
        dvParameters.saveParameters(self.dv, sP.toDict())
        dvParameters.saveParameters(self.dv, xP.toDict())


    def finalize(self):
        self.pulser.switch_manual('wireVoltage',False)

    def __del__(self):
        self.cxn.disconnect()

if __name__ == '__main__':
    numCycles = 4.0
    frequency = 50.0
    excitationTime = numCycles/frequency
    binTime = excitationTime  / 153.0
    iterations = int(20* (frequency/10.0))
    bufferTime = 1.0/frequency
    print iterations
    print frequency
    params = {
        'excitationTime':excitationTime,
        'bufferTime':bufferTime
        }

    exprtParams = {
        'iterations':iterations,
        'binTime': binTime
        }

    exprt = WireVoltageModulation(params, exprtParams)
    exprt.run()
