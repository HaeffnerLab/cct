import labrad
from labrad import types
import numpy
import time
import datetime

from scriptLibrary import dvParameters

class TickleExperiment(SemaphoreExperiment):

    experimentName = 'Tickle_Compensation'

    def __init__(self, seqParams, exprtParams):

        self.cxn = labrad.connect()
        self.cxnlab = labrad.connect('192.168.169.49')

        self.dv = self.cxn.data_vault
        self.pulser = self.cxn.pulser
        self.seqP = Bunch(**seqParams)
        self.expP = Bunch(**exprtParams)

        self.experimentPath = ['Compensation', 'Tickle']
        self.experimentLabel = 'TickleCompensation'

    
    def initialize(self):

        
