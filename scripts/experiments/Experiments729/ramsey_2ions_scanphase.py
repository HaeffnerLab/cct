from common.abstractdevices.script_scanner.scan_methods import experiment
from excitations import excitation_ramsey_2ions
from cct.scripts.scriptLibrary.common_methods_729 import common_methods_729 as cm
from cct.scripts.scriptLibrary import dvParameters
import time
import labrad
from labrad.units import WithUnit
from numpy import linspace

class ramsey_2ions_phase(experiment):
    
    name = 'Ramsey2ions_ScanPhase'
    ramsey2ions_required_parameters = [
                           ('Ramsey2ions_ScanGapParity', 'scangap'),
                           ('Ramsey2ions_ScanGapParity', 'first_ion_number'),
                           ('Ramsey2ions_ScanGapParity', 'second_ion_number'),
                           ('Ramsey2ions_ScanGapParity', 'line_selection'),
                           ('StateReadout', 'parity_threshold_high'),
                           ('StateReadout', 'parity_threshold_low')
                           ]
    @classmethod
    def all_required_parameters(cls):
        parameters = set(cls.ramsey2ions_required_parameters)
        parameters = parameters.union(set(excitation_ramsey_2ions.all_required_parameters()))
        parameters = list(parameters)
        #removing parameters we'll be overwriting, and they do not need to be loaded
        parameters.remove(('Ramsey_2ions','excitation_frequency'))
        parameters.remove(('Ramsey_2ions','ramsey_time'))
        return parameters

        