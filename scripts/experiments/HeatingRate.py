import sys;
sys.path.append('/home/cct/LabRAD/cct/scripts')
sys.path.append('/home/cct/LabRAD/cct/PulseSequences')
import labrad
from labrad import types
import numpy
import time
from scriptLibrary import dvParameters
from PulseSequences.heat import HeatSeq
from fly_processing import Binner

class Bunch:
    def __init__(self, **kwds):
        self.__dict__.update(kwds)
    
    def __setitem__(self, key, val):
        self.__dict__[key] = val
    
    def toDict(self):
        return self.__dict__
        
class Heat():
    experimentName = 'Heat_Auto'
    
    def __init__(self, seqParams, exprmtParams):
	self.cxn = labrad.connect()
	self.cxnlab = labrad.connect('192.168.169.49') #connection to labwide network
	self.dv = self.cxn.data_vault
	self.pulser = self.cxn.pulser
	self.pmt = self.cxn.normalpmtflow
	self.seqP = Bunch(**seqParams)
	self.expP = Bunch(**exprtParams)
	self.Binner = None      
	
def initialize(self):
        #directory name and initial variables
        self.dirappend = time.strftime("%Y%m%d_%H%M_%S",time.localtime())
        self.topdirectory = time.strftime("%Y%m%d",time.localtime())
        self.setupLogic()
        #get the count rate for the crystal at the same parameters as crystallization
        self.programPulser()
        #data processing setup
        self.Binner = Binner(self.seqP.recordTime, self.expP.binTime)
        
def setupLogic(self):
        self.pulser.switch_auto('axial', True) #axial needs to be inverted, so that high TTL corresponds to light ON
        self.pulser.switch_auto('110DP', False) #high TTL corresponds to light OFF
        self.pulser.switch_auto('866DP', False) #high TTL corresponds to light OFF
        
def programPulser(self):
        seq = HeatSeq(self.pulser)
        self.pulser.new_sequence()
        seq.setVariables(**self.seqP.toDict())
        seq.defineSequence()
        self.pulser.program_sequence()
        self.seqP['recordTime'] = seq.parameters.recordTime
        self.seqP['startReadout'] = seq.parameters.startReadout
        self.seqP['endReadout'] = seq.parameters.endReadout
        
def run(self):
        self.initialize()
        self.sequence()
        self.finalize()
        print 'DONE {}'.format(self.dirappend)     
        
def sequence(self):
        sP = self.seqP
        xP = self.expP
        #saving timetags
        self.dv.cd(['','Experiments', self.experimentName, self.topdirectory, self.dirappend], True)
        self.dv.new('timetags',[('Time', 'sec')],[('PMT counts','Arb','Arb')] )
        #do iterations
        for iteration in range(xP.iterations):
            print 'recording trace {0} out of {1}'.format(iteration+1, xP.iterations)
            self.pulser.reset_timetags()
            self.pulser.start_single()
            self.pulser.wait_sequence_done()
            self.pulser.stop_sequence()
            timetags = self.pulser.get_timetags().asarray
            iters = iteration * numpy.ones_like(timetags)
            self.dv.add(numpy.vstack((iters,timetags)).transpose())
            #add to binning of the entire sequence
            self.Binner.add(timetags)           
        #adding binned fluorescence to data vault:
        binX, binY = self.Binner.getBinned()
        self.dv.cd(['', self.topdirectory, 'Experiments', self.experimentName, self.dirappend])
        self.dv.new('binned',[('Time', 'sec')], [('PMT counts','Arb','Arb')] )
        data = numpy.vstack((binX, binY)).transpose()
        self.dv.add(data)
        self.dv.add_parameter('Window',['Binned Fluorescence'])
        self.dv.add_parameter('plotLive',True)
        # gathering parameters and adding them to data vault
        measureList = ['trapdrive','endcaps','compensation','dcoffsetonrf','cavity397','cavity866','multiplexer397','multiplexer866','axialDP', 'pulser']
        measuredDict = dvParameters.measureParameters(self.cxn, self.cxnlab, measureList)
        dvParameters.saveParameters(self.dv, measuredDict)
        dvParameters.saveParameters(self.dv, sP.toDict())
        dvParameters.saveParameters(self.dv, xP.toDict())        
        
        
def finalize(self):
        for name in ['axial', '110DP']:
            self.pulser.switch_manual(name)        
            
if __name__ == '__main__':
    #experiment parameters
    params = {
        'initial_cooling': 25e-3,
    }
    exprtParams = {
       'iterations':25,
       'pmtresolution':0.075,
       'detect_time':0.225,
       'binTime':250.0*10**-6,
       'threshold':35000,

    }
    exprt = LatentHeat(params,exprtParams)
    exprt.run()            