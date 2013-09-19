from common.okfpgaservers.pulser.pulse_sequences.pulse_sequence import pulse_sequence
from SidebandCooling import sideband_cooling
from labrad.units import WithUnit
from treedict import TreeDict

class sideband_precooling(pulse_sequence):
    
    required_parameters = [
                           ('SidebandPrecooling','sideband_precooling_cycles'),
                           ('SidebandPrecooling','sideband_precooling_optical_pumping_duration'),
                           ('SidebandPrecooling','sideband_precooling_amplitude_866'),
                           ('SidebandPrecooling','sideband_precooling_amplitude_854'),
                           ('SidebandPrecooling','sideband_precooling_amplitude_729'),
                           ('SidebandPrecooling','sideband_precooling_frequency_854'),
                           ('SidebandPrecooling', 'sideband_precooling_frequency_866'),
                           ('SidebandPrecooling', 'sideband_precooling_frequency_729'),
                           ('SidebandPrecooling', 'sideband_precooling_detuning_729'),
                           ('SidebandPrecooling','sideband_precooling_continuous_duration'),
                           ]
    
    required_subsequences = [sideband_cooling]

    def sequence(self):
        replace = self.make_replace()
        self.addSequence(sideband_cooling, TreeDict.fromDict(replace))

    def make_replace(self):
        sc = self.parameters.SidebandPrecooling

        replace = {
            'SidebandCooling.sideband_cooling_cycles':sc.sideband_precooling_cycles,
            'SidebandCooling.sideband_cooling_type':'continuous',
            'SidebandCooling.sideband_cooling_duration_729_increment_per_cycle':WithUnit(0.0,'us'),
            'SidebandCooling.sideband_cooling_optical_pumping_duration':sc.sideband_precooling_optical_pumping_duration,
            'SidebandCooling.sideband_cooling_amplitude_866':sc.sideband_precooling_amplitude_866,
            'SidebandCooling.sideband_cooling_amplitude_854':sc.sideband_precooling_amplitude_854,
            'SidebandCooling.sideband_cooling_amplitude_729':sc.sideband_precooling_amplitude_729,
            'SidebandCooling.sideband_cooling_frequency_854':sc.sideband_precooling_frequency_854,
            'SidebandCooling.sideband_cooling_frequency_866':sc.sideband_precooling_frequency_866,
            'SidebandCooling.sideband_cooling_frequency_729':sc.sideband_precooling_frequency_729,
            'SidebandCooling.sideband_cooling_detuning_729':sc.sideband_precooling_detuning_729,
            'SidebandCoolingContinuous.sideband_cooling_continuous_duration',sideband_precooling_continuous_duration,
            'SidebandCoolingPulsed.sideband_cooling_pulsed_duration_729', sideband_precooling_continuous_duration
            }

        return replace
