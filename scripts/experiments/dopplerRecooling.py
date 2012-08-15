# heating rate measurement by Doppler recooling

import sys
sys.path.append('/home/cct/LabRAD/cct/scripts')
sys.path.append('/home/cct/LabRAD/cct/scripts/PulseSequences')

import labrad
from labrad import types
import numpy
import time

from flyProcessing import Binner
from PulseSequences.dopplerRecooling import DopplerRecool

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
        
        self.dv = self.cxn.data_vault
        self.pulser = self.cxn.pulser
        self.pmt = self.cxn.normalpmtflow
        self.seqP = Bunch(**seqParams)
        self.expP = Bunch(**exprtParams)
        self.Binner = None

    def initialize(self):
        pass

    def setupLogic(self):
        pass

    def programPulser(self):
        seq = DopplerRecool(self.pulser)
        self.pulser.new_sequence()
        seq.setVariables(**self.seqP.toDict())
        seq.defineSequence()
        self.pulser.program_sequence()
        self.seqP['recordTime'] = seq.parameters.recordTime
        self.seqP['darkTime'] = seq.parameters.darkTime

    def run(self):
        self.initialize()
        self.sequence()
        self.finalize()
        print "done"
