from common.okfpgaservers.pulser.pulse_sequences.pulse_sequence import pulse_sequence
from RepumpD import repump_d
from DopplerCooling import doppler_cooling
from treedict import TreeDict

from common.okfpgaservers.pulser.pulse_sequences.pulse_sequence import pulse_sequence
from RepumpD import repump_d
from DopplerCooling import doppler_cooling
from treedict import TreeDict

class doppler_cooling_with_mode_coupling(pulse_sequence):
    
    required_parameters = [('DopplerCooling','doppler_cooling_duration')]
    required_subsequences = [repump_d, doppler_cooling]
    replaced_parameters = {doppler_cooling:[('DopplerCooling','doppler_cooling_duration')]
                           }
    
    def sequence(self):
        dc_duration = self.parameters.DopplerCooling.doppler_cooling_duration
        #add the sequence
        self.addSequence(repump_d)
        stop_repump_d = self.end
        replacement = TreeDict.fromdict({'DopplerCooling.doppler_cooling_duration':stop_repump_d + dc_duration})
        self.addSequence(doppler_cooling, replacement, position = self.start)


class doppler_cooling_with_mode_coupling(pulse_sequence):
    
    required_parameters = [
    	('DopplerCooling','doppler_cooling_duration'),
    	('ParametricCoupling', 'mode_swapping_time'),
    	('DopplerCooling', 'mode_swapping_cycles')
    	]
    required_subsequences = [repump_d, doppler_cooling]
    
    def sequence(self):
        dc_duration = self.parameters.DopplerCooling.doppler_cooling_duration
        ti = self.parameters.ParametricCoupling.mode_swapping_time
        ncycles = self.parameters.DopplerCooling.mode_swapping_cycles
        delta_t = dc_duration / ncycles

        swap_times = [self.start + i*delta_t for i in range(int(ncycles))]

        # make sure we're not swapping for too long
        while (swap_times[-1] + ti) >= dc_duration:
        	swap_times.pop()

        #add the sequence
        self.addSequence(repump_d)
        stop_repump_d = self.end
        replacement = TreeDict.fromdict({'DopplerCooling.doppler_cooling_duration':stop_repump_d + dc_duration})
        self.addSequence(doppler_cooling, replacement, position = self.start)
        for j in swap_times:
        	self.addTTL('parametric_modulation', j, ti)