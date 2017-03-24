from cct.scripts.PulseSequences.spectrum_rabi import spectrum_rabi
from commmon.okfpgaservers.pulser.pulse_sequences.plot_sequence import SequencePlotter
from labrad.units import WithUnit

if __name__ == '__main__':
    import labrad
    cxn = labrad.connect()
    import time
    from treedict import TreeDict
    params = test_parameters.parameters
    d = TreeDict()
    