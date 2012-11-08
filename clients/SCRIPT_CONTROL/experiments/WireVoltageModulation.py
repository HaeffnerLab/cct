# wire voltage modulation

import sys
import labrad
from labrad import types
import numpy
import time
import datetime
import sys
sys.path.append('/home/cct/LabRAD/cct/')
from fly_processing import Binner
from scripts.PulseSequences.wireVoltageMod import wireVoltage
from scripts.scriptLibrary import dvParameters
from scripts.experiments import SemaphoreExperiment

# class Bunch:
#     def __init__(self, **kwds):
#         self.__dict__.update(kwds)
    
#     def __setitem__(self, key, val):
#         self.__dict__[key] = val
    
#     def toDict(self):
#         return self.__dict__


class WireVoltageModulation(SemaphoreExperiment):
    def __init__(self, c, d): 
        self.experimentPath = ['Wire', 'WireVoltageModulation']

    def run(self):
        self.initialize()
        try:
            self.sequence()
        except Exception,e:
            print 'Had to stop Sequence with error:', e
        finally:
            self.finalize()
        
        
    def initialize(self):
        print 'Started: {}'.format(self.experimentPath)
        self.percentDone = 0.
        self.importLabrad()
        # self.setupDataVault()
        self.sequenceParameters = self.setup_sequence_parameters()
        self.dirappend = time.strftime("%Y%m%d_%H%M_%S",time.localtime())
        self.topdirectory = time.strftime("%Y%m%d",time.localtime())
        self.setupPulser()
        self.programPulser()
        
        totalBinningTime = 5e-3 + self.seqP.bufferTime + self.seqP.excitationTime
        self.Binner = Binner(totalBinningTime, self.sequenceParameters['binTime'])

    def importLabrad(self):
        self.cxn = labrad.connect()
        self.cxnlab = labrad.connect('192.168.169.49') # labwide network
        self.dv = self.cxn.data_vault
        self.pulser = self.cxn.pulser
        self.sem = cxn.semaphore
        self.p = populate_parameters(self.sem, self.experimentPath)

    def setupPulser(self):
        self.pulser.switch_auto('wireVoltage', False)

    def programPulser(self):
        seq = wireVoltage(**self.sequenceParameters)
        seq.programSequence(self.pulser)

    def setup_sequence_parameters(self):
        sequence_parameters = {}.fromkeys(sample_parameters.parameters)
        check = self.check_parameter
        common_values = dict([(key,check(value)) for key,value in self.p.iteritems() if key in sequence_parameters])
        sequence_paremters.update(common_values)
        sequence_parameters['excitationTime'] = self.check_parameter(self.p.excitationTime)
        sequence_parameters['bufferTime'] = self.check_parameter(self.p.bufferTime)
        sequence_parameters['iterations'] = self.check_parameter(self.p.iterations)
        sequence_parameters['binTime'] = self.check_parameter(self.p.binTimesssssssssssss)

    def sequence(self):

        sP = self.seqP
        xP = self.expP
        iterations = self.sequenceParameters['iterations']
        
        now = datetime.datetime.now()
        date = now.strftime("%Y%m%d")
        ti = now.strftime('%H%M%S')

        timetag_context = self.dv.context()
        self.dv.cd(['',date, self.experimentPath[1], ti, 'binned'], True)
        self.dv.cd(['',date, self.experimentPath[1], ti, 'timetags'], True, context = timetag_context)
        #self.dv.new('binned_timetags',[('Time', 'sec')],[('PMT counts','Arb','Arb')] )
        self.dv.new('timetags',[('Time', 'sec')], [('Iteration', 'Arb','Arb')] , context = timetag_context )

        numUpdates = 1

        for n in range(numUpdates):
            for iteration in range(iterations / numUpdates):

                self.pulser.reset_timetags()
                self.pulser.start_single()
                self.pulser.wait_sequence_done()
                self.pulser.stop_sequence()
                timetags = self.pulser.get_timetags().asarray
                iterationUmber = (n*(iterations/numUpdates) + iteration) * numpy.ones(len(timetags))
                timetag_raw = numpy.vstack((iterationUmber,timetags)).transpose()
                self.dv.add( timetag_raw, context=timetag_context)
                print n*(iterations/numUpdates) + iteration
                self.Binner.add(timetags)
            
            self.dv.new('binned_timetags_' + str(n+1) + '_of_' + str(numUpdates),[('Time', 'sec')],[('PMT counts','Arb','Arb')] )
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
    exprt = WireVoltageModulation()
    exprt.run()
