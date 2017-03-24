from common.okfpgaservers.pulser.pulse_sequences.pulse_sequence import pulse_sequence
from OpticalPumping import optical_pumping
from SidebandCoolingContinuous import sideband_cooling_continuous
from SidebandCoolingPulsed import sideband_cooling_pulsed
from treedict import TreeDict

class sideband_cooling(pulse_sequence):
    
    required_parameters = [
                           ('SidebandCooling','sideband_cooling_cycles'),
                           ('SidebandCooling','sideband_cooling_type'),
                           ('SidebandCooling','sideband_cooling_duration_729_increment_per_cycle'),
                           ('SidebandCooling','sideband_cooling_optical_pumping_duration'),
                           ('SidebandCooling','sideband_cooling_amplitude_866'),
                           ('SidebandCooling','sideband_cooling_amplitude_854'),
                           ('SidebandCooling','sideband_cooling_amplitude_729'),
                           ('SidebandCooling','sideband_cooling_frequency_854'),
                           ('SidebandCooling', 'sideband_cooling_frequency_866'),
                           ('SidebandCooling', 'sideband_cooling_frequency_729'),
                           ('SidebandCooling', 'stark_shift'),
                           ('SidebandCoolingContinuous','sideband_cooling_continuous_duration'),
                           ('SidebandCoolingPulsed','sideband_cooling_pulsed_duration_729'),
                           
                           ('SequentialSBCooling','enable'),
                           ('SequentialSBCooling','additional_stages'),
                           ('SequentialSBCooling', 'interleave'),
                           ('SequentialSBCooling','stage2_amplitude_729'),
                           ('SequentialSBCooling','stage2_amplitude_854'),
                           ('SequentialSBCooling','stage2_frequency_729'),
                           ('SequentialSBCooling','stage3_amplitude_729'),
                           ('SequentialSBCooling','stage3_amplitude_854'),
                           ('SequentialSBCooling','stage3_frequency_729'),
                           ('SequentialSBCooling','stage4_amplitude_729'),
                           ('SequentialSBCooling','stage4_amplitude_854'),
                           ('SequentialSBCooling','stage4_frequency_729'),
                           ('SequentialSBCooling','stage5_amplitude_729'),
                           ('SequentialSBCooling','stage5_amplitude_854'),
                           ('SequentialSBCooling','stage5_frequency_729'),
                           ]
    
    required_subsequences = [sideband_cooling_continuous, sideband_cooling_pulsed, optical_pumping]
    replaced_parameters = {
                           sideband_cooling_continuous:[
                                                        ('SidebandCoolingContinuous','sideband_cooling_continuous_duration'),
                                                        ('SidebandCoolingContinuous','sideband_cooling_continuous_frequency_854'),
                                                        ('SidebandCoolingContinuous','sideband_cooling_continuous_frequency_729'),
                                                        ('SidebandCoolingContinuous','sideband_cooling_continuous_frequency_866'),
                                                        ('SidebandCoolingContinuous','sideband_cooling_continuous_amplitude_854'),
                                                        ('SidebandCoolingContinuous','sideband_cooling_continuous_amplitude_729'),
                                                        ('SidebandCoolingContinuous','sideband_cooling_continuous_amplitude_866'),
                                                        ],
                            sideband_cooling_pulsed:[
                                                        ('SidebandCoolingPulsed','sideband_cooling_pulsed_duration_729'),
                                                        ('SidebandCoolingPulsed','sideband_cooling_pulsed_frequency_854'),
                                                        ('SidebandCoolingPulsed','sideband_cooling_pulsed_amplitude_854'),
                                                        ('SidebandCoolingPulsed','sideband_cooling_pulsed_frequency_729'),
                                                        ('SidebandCoolingPulsed','sideband_cooling_pulsed_amplitude_729'),
                                                        ('SidebandCoolingPulsed','sideband_cooling_pulsed_frequency_866'),
                                                        ('SidebandCoolingPulsed','sideband_cooling_pulsed_amplitude_866'),
                                                        ],
                           optical_pumping:[
                                            ('OpticalPumping','optical_pumping_continuous'),
                                            ('OpticalPumpingContinuous','optical_pumping_continuous_duration')
                                            ]
                           }
    
    def sequence(self):
        '''
        sideband cooling pulse sequence consists of multiple sideband_cooling_cycles where each cycle consists 
        of a period of sideband cooling followed by continuous optical pumping. 
        
        sideband cooling can be either pulsed or continuous 
        '''
        sc = self.parameters.SidebandCooling
        sc2 = self.parameters.SequentialSBCooling
        if sc.sideband_cooling_type == 'continuous':
            continuous = True
        elif sc.sideband_cooling_type == 'pulsed':
            continuous = False
        else:
            raise Exception ("Incorrect Sideband cooling type {0}".format(sc.sideband_cooling_type))
        
        if continuous:
            cooling = sideband_cooling_continuous
            duration_key = 'SidebandCoolingContinuous.sideband_cooling_continuous_duration'
            cooling_replace = {
                               'SidebandCoolingContinuous.sideband_cooling_continuous_duration':self.parameters.SidebandCoolingContinuous.sideband_cooling_continuous_duration,
                               'SidebandCoolingContinuous.sideband_cooling_continuous_frequency_854':sc.sideband_cooling_frequency_854,
                               'SidebandCoolingContinuous.sideband_cooling_continuous_frequency_729':sc.sideband_cooling_frequency_729 + sc.stark_shift,
                               'SidebandCoolingContinuous.sideband_cooling_continuous_frequency_866':sc.sideband_cooling_frequency_866,
                               'SidebandCoolingContinuous.sideband_cooling_continuous_amplitude_854':sc.sideband_cooling_amplitude_854,
                               'SidebandCoolingContinuous.sideband_cooling_continuous_amplitude_729':sc.sideband_cooling_amplitude_729,
                               'SidebandCoolingContinuous.sideband_cooling_continuous_amplitude_866':sc.sideband_cooling_amplitude_866,
                               }
            
            cooling_replace_2 = cooling_replace.copy()
            cooling_replace_2['SidebandCoolingContinuous.sideband_cooling_continuous_frequency_729'] = sc2.stage2_frequency_729 + sc.stark_shift
            cooling_replace_2['SidebandCoolingContinuous.sideband_cooling_continuous_amplitude_729'] = sc2.stage2_amplitude_729      
            cooling_replace_2['SidebandCoolingContinuous.sideband_cooling_continuous_amplitude_854'] = sc2.stage2_amplitude_854              
            
            cooling_replace_3 = cooling_replace.copy()
            cooling_replace_3['SidebandCoolingContinuous.sideband_cooling_continuous_frequency_729'] = sc2.stage3_frequency_729 + sc.stark_shift
            cooling_replace_3['SidebandCoolingContinuous.sideband_cooling_continuous_amplitude_729'] = sc2.stage3_amplitude_729      
            cooling_replace_3['SidebandCoolingContinuous.sideband_cooling_continuous_amplitude_854'] = sc2.stage3_amplitude_854 
            
            cooling_replace_4 = cooling_replace.copy()
            cooling_replace_4['SidebandCoolingContinuous.sideband_cooling_continuous_frequency_729'] = sc2.stage4_frequency_729 + sc.stark_shift
            cooling_replace_4['SidebandCoolingContinuous.sideband_cooling_continuous_amplitude_729'] = sc2.stage4_amplitude_729      
            cooling_replace_4['SidebandCoolingContinuous.sideband_cooling_continuous_amplitude_854'] = sc2.stage4_amplitude_854             
            
            cooling_replace_5 = cooling_replace.copy()        
            cooling_replace_5['SidebandCoolingContinuous.sideband_cooling_continuous_frequency_729'] = sc2.stage5_frequency_729 + sc.stark_shift
            cooling_replace_5['SidebandCoolingContinuous.sideband_cooling_continuous_amplitude_729'] = sc2.stage5_amplitude_729      
            cooling_replace_5['SidebandCoolingContinuous.sideband_cooling_continuous_amplitude_854'] = sc2.stage5_amplitude_854     
            
        else:
            #pulsed
            cooling = sideband_cooling_pulsed
            duration_key = 'SidebandCoolingPulsed.sideband_cooling_pulsed_duration_729'
            cooling_replace = {
                                'SidebandCoolingPulsed.sideband_cooling_pulsed_duration_729':self.parameters.SidebandCoolingPulsed.sideband_cooling_pulsed_duration_729,
                                'SidebandCoolingPulsed.sideband_cooling_pulsed_frequency_854':sc.sideband_cooling_frequency_854,
                                'SidebandCoolingPulsed.sideband_cooling_pulsed_amplitude_854':sc.sideband_cooling_amplitude_854,
                                'SidebandCoolingPulsed.sideband_cooling_pulsed_frequency_729':sc.sideband_cooling_frequency_729 + sc.stark_shift,
                                'SidebandCoolingPulsed.sideband_cooling_pulsed_amplitude_729':sc.sideband_cooling_amplitude_729,
                                'SidebandCoolingPulsed.sideband_cooling_pulsed_frequency_866':sc.sideband_cooling_frequency_866,
                                'SidebandCoolingPulsed.sideband_cooling_pulsed_amplitude_866':sc.sideband_cooling_amplitude_866,
                               }
            
            cooling_replace_2 = cooling_replace.copy()
            cooling_replace_2['SidebandCoolingPulsed.sideband_cooling_pulsed_frequency_729'] = sc2.stage2_frequency_729 + sc.stark_shift
            cooling_replace_2['SidebandCoolingPulsed.sideband_cooling_pulsed_amplitude_729'] = sc2.stage2_amplitude_729      
            cooling_replace_2['SidebandCoolingPulsed.sideband_cooling_pulsed_amplitude_854'] = sc2.stage2_amplitude_854              
            
            cooling_replace_3 = cooling_replace.copy()
            cooling_replace_3['SidebandCoolingPulsed.sideband_cooling_pulsed_frequency_729'] = sc2.stage3_frequency_729 + sc.stark_shift
            cooling_replace_3['SidebandCoolingPulsed.sideband_cooling_pulsed_amplitude_729'] = sc2.stage3_amplitude_729      
            cooling_replace_3['SidebandCoolingPulsed.sideband_cooling_pulsed_amplitude_854'] = sc2.stage3_amplitude_854 
            
            cooling_replace_4 = cooling_replace.copy()
            cooling_replace_4['SidebandCoolingPulsed.sideband_cooling_pulsed_frequency_729'] = sc2.stage4_frequency_729 + sc.stark_shift
            cooling_replace_4['SidebandCoolingPulsed.sideband_cooling_pulsed_amplitude_729'] = sc2.stage4_amplitude_729      
            cooling_replace_4['SidebandCoolingPulsed.sideband_cooling_pulsed_amplitude_854'] = sc2.stage4_amplitude_854             
            
            cooling_replace_5 = cooling_replace.copy()        
            cooling_replace_5['SidebandCoolingPulsed.sideband_cooling_pulsed_frequency_729'] = sc2.stage5_frequency_729 + sc.stark_shift
            cooling_replace_5['SidebandCoolingPulsed.sideband_cooling_pulsed_amplitude_729'] = sc2.stage5_amplitude_729      
            cooling_replace_5['SidebandCoolingPulsed.sideband_cooling_pulsed_amplitude_854'] = sc2.stage5_amplitude_854     
            
            
        optical_pump_replace = {
                                'OpticalPumping.optical_pumping_continuous':True,
                                'OpticalPumpingContinuous.optical_pumping_continuous_duration':sc.sideband_cooling_optical_pumping_duration,
                                }
        Nc = int(sc.sideband_cooling_cycles)
        sequential_cooling_replacements = [cooling_replace_2,cooling_replace_3,cooling_replace_4,cooling_replace_5]
        if sc2.interleave:
            for i in range(int(sc.sideband_cooling_cycles)):
                #each cycle, increment the 729 duration
                cooling_replace[duration_key] +=  sc.sideband_cooling_duration_729_increment_per_cycle
                self.addSequence(cooling, TreeDict.fromdict(cooling_replace))
                for j in range(1,5):
                    if sc2.enable and j <= sc2.additional_stages:
                        cooling_stage_replace = sequential_cooling_replacements[j-1]
                        self.addSequence(cooling, TreeDict.fromdict(cooling_stage_replace))
                        cooling_stage_replace[duration_key] +=  sc.sideband_cooling_duration_729_increment_per_cycle
                self.addSequence(optical_pumping, TreeDict.fromdict(optical_pump_replace))
        if not sc2.interleave:
            for i in range(int(sc.sideband_cooling_cycles)):
                #each cycle, increment the 729 duration
                cooling_replace[duration_key] +=  sc.sideband_cooling_duration_729_increment_per_cycle
                self.addSequence(cooling, TreeDict.fromdict(cooling_replace))
            for j in range(1,5):
                for i in range(int(sc.sideband_cooling_cycles)):
                    if sc2.enable and j <= sc2.additional_stages:
                        cooling_stage_replace = sequential_cooling_replacements[j-1]
                        self.addSequence(cooling, TreeDict.fromdict(cooling_stage_replace))
                        cooling_stage_replace[duration_key] +=  sc.sideband_cooling_duration_729_increment_per_cycle
            self.addSequence(optical_pumping, TreeDict.fromdict(optical_pump_replace))           
