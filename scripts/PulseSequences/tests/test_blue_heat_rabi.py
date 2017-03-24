from labrad.units import WithUnit
from common.okfpgaservers.pulser.pulse_sequences.plot_sequence import SequencePlotter
from space_time.scripts.PulseSequences.blue_heat_rabi import blue_heat_rabi as tested_sequence

class test_parameters(object):
    
    parameters = {
              ('RepumpD_5_2','repump_d_duration'):WithUnit(200, 'us'),
              ('RepumpD_5_2','repump_d_frequency_854'):WithUnit(80.0, 'MHz'),
              ('RepumpD_5_2','repump_d_amplitude_854'):WithUnit(-11.0, 'dBm'),
              
              ('DopplerCooling', 'doppler_cooling_frequency_397'):WithUnit(90.0, 'MHz'),
              ('DopplerCooling', 'doppler_cooling_amplitude_397'):WithUnit(-15.0, 'dBm'),
              ('DopplerCooling', 'doppler_cooling_frequency_866'):WithUnit(80.0, 'MHz'),
              ('DopplerCooling', 'doppler_cooling_amplitude_866'):WithUnit(-11.0, 'dBm'),
              ('DopplerCooling', 'doppler_cooling_repump_additional'):WithUnit(100, 'us'),
              ('DopplerCooling', 'doppler_cooling_duration'):WithUnit(1.0,'ms'),
              
              ('OpticalPumping','optical_pumping_enable'):True,
              ('OpticalPumping','optical_pumping_frequency_729'):WithUnit(0.0, 'MHz'),
              ('OpticalPumping','optical_pumping_frequency_854'):WithUnit(80.0, 'MHz'),
              ('OpticalPumping','optical_pumping_frequency_866'):WithUnit(80.0, 'MHz'),
              ('OpticalPumping','optical_pumping_amplitude_729'):WithUnit(-10.0, 'dBm'),
              ('OpticalPumping','optical_pumping_amplitude_854'):WithUnit(-5.0, 'dBm'),
              ('OpticalPumping','optical_pumping_amplitude_866'):WithUnit(-11.0, 'dBm'),
              ('OpticalPumping','optical_pumping_type'):'continuous',
              
              ('OpticalPumpingContinuous','optical_pumping_continuous_duration'):WithUnit(1, 'ms'),
              ('OpticalPumpingContinuous','optical_pumping_continuous_repump_additional'):WithUnit(200, 'us'),
              
              ('OpticalPumpingPulsed','optical_pumping_pulsed_cycles'):2.0,
              ('OpticalPumpingPulsed','optical_pumping_pulsed_duration_729'):WithUnit(20, 'us'),
              ('OpticalPumpingPulsed','optical_pumping_pulsed_duration_repumps'):WithUnit(20, 'us'),
              ('OpticalPumpingPulsed','optical_pumping_pulsed_duration_additional_866'):WithUnit(20, 'us'),
              ('OpticalPumpingPulsed','optical_pumping_pulsed_duration_between_pulses'):WithUnit(5, 'us'),

              ('SidebandCooling','sideband_cooling_enable'):True,
              ('SidebandCooling','sideband_cooling_cycles'): 4.0,
              ('SidebandCooling','sideband_cooling_type'):'continuous',
              ('SidebandCooling','sideband_cooling_duration_729_increment_per_cycle'):WithUnit(0, 'us'),
              ('SidebandCooling','sideband_cooling_frequency_854'):WithUnit(80.0, 'MHz'),
              ('SidebandCooling','sideband_cooling_amplitude_854'):WithUnit(-11.0, 'dBm'),
              ('SidebandCooling','sideband_cooling_frequency_866'):WithUnit(80.0, 'MHz'),
              ('SidebandCooling','sideband_cooling_amplitude_866'):WithUnit(-11.0, 'dBm'),
              ('SidebandCooling','sideband_cooling_frequency_729'):WithUnit(-10.0, 'MHz'),
              ('SidebandCooling','sideband_cooling_amplitude_729'):WithUnit(-11.0, 'dBm'),
              ('SidebandCooling','sideband_cooling_optical_pumping_duration'):WithUnit(500, 'us'),
              
              ('SidebandCoolingContinuous','sideband_cooling_continuous_duration'):WithUnit(500, 'us'),
              
              ('SidebandCoolingPulsed','sideband_cooling_pulsed_duration_729'):WithUnit(10, 'us'),
              ('SidebandCoolingPulsed','sideband_cooling_pulsed_cycles'):10.0,
              ('SidebandCoolingPulsed','sideband_cooling_pulsed_duration_repumps'):WithUnit(10, 'us'),
              ('SidebandCoolingPulsed','sideband_cooling_pulsed_duration_additional_866'):WithUnit(10, 'us'),
              ('SidebandCoolingPulsed','sideband_cooling_pulsed_duration_between_pulses'):WithUnit(5, 'us'),
       
              ('Heating', 'blue_heating_type'):'local',
              ('Heating', 'blue_heating_delay_before'):WithUnit(10.0, 'us'),
              ('Heating', 'blue_heating_delay_after'):WithUnit(10.0, 'us'),
              ('Heating', 'blue_heating_duration'):WithUnit(10.0, 'us'),
              ('Heating', 'blue_heating_repump_additional'):WithUnit(10.0, 'us'),
              ('Heating', 'global_blue_heating_amplitude_397'):WithUnit(-17.0, 'dBm'),
              ('Heating', 'global_blue_heating_frequency_397'):WithUnit(100.0, 'MHz'),
              ('Heating', 'local_blue_heating_amplitude_397'):WithUnit(-17.0, 'dBm'),
              ('Heating', 'local_blue_heating_frequency_397'):WithUnit(100.0, 'MHz'),
              ('Heating', 'blue_heating_frequency_866'):WithUnit(80.0, 'MHz'),
              ('Heating', 'blue_heating_amplitude_866'):WithUnit(-15.0, 'dBm'),
              
              ('Excitation_729','rabi_excitation_frequency'):WithUnit(10.0, 'MHz'),
              ('Excitation_729','rabi_excitation_amplitude'):WithUnit(-5.0, 'dBm'),
              ('Excitation_729','rabi_excitation_duration'):WithUnit(10.0, 'us'),
              ('Excitation_729','rabi_excitation_phase'):WithUnit(0.0, 'deg'),
              
              ('StateReadout','state_readout_frequency_397'):WithUnit(90.0, 'MHz'),
              ('StateReadout','state_readout_amplitude_397'):WithUnit(-13.0, 'dBm'),
              ('StateReadout','state_readout_frequency_866'):WithUnit(80.0, 'MHz'),
              ('StateReadout','state_readout_amplitude_866'):WithUnit(-11.0, 'dBm'),
              ('StateReadout','state_readout_duration'):WithUnit(3.0,'ms'),
              ('StateReadout','use_camera_for_readout'):True,
                  
              ('Tomography', 'rabi_pi_time'):WithUnit(50.0, 'us'),
              ('Tomography', 'iteration'):0,
              ('Tomography', 'tomography_excitation_frequency'):WithUnit(0.0, 'MHz'),
              ('Tomography', 'tomography_excitation_amplitude'):WithUnit(-11.0, 'dBm'),
              }

if __name__ == '__main__':
    import labrad
    cxn = labrad.connect()
    import time
    from treedict import TreeDict
    params = test_parameters.parameters
    d = TreeDict()
    #make a treedictionary out of the parameters
    for (collection,param), value in test_parameters.parameters.iteritems():
        d['{0}.{1}'.format(collection, param)] = value
        if not (collection,param) in tested_sequence.required_parameters:
            print 'parameter not listed among requirments', collection, param
    for key in d.keys():
        a = TreeDict()
        a.update(d)
        a.pop(key)
        try:
            sequence = tested_sequence(a)
        except Exception:
            pass
        else:
            print 'key not needed', key
    tinit = time.time()
    cs = tested_sequence(d)
    cs.programSequence(cxn.pulser)
    print 'to program', time.time() - tinit
#    cxn.pulser.start_number(10)
#    cxn.pulser.wait_sequence_done()
#    cxn.pulser.stop_sequence()
    dds = cxn.pulser.human_readable_dds()
    ttl = cxn.pulser.human_readable_ttl()
    ttl_result = [['0.0', '00000000000000000000000000000000'], ['1e-05', '00000000000000000010000000000000'], ['1.008e-05', '00000000000000000000000000000000'], ['6e-05', '00000000000000000010000000000000'], ['6.008e-05', '00000000000000000000000000000000'], ['0.00026', '00000000000000000010000000000000'], ['0.00026008', '00000000000000000000000000000000'], ['0.00132', '00000000000000000010000000000000'], ['0.00132008', '00000000000000000000000000000000'], ['0.00142', '00000000000000000010000000000000'], ['0.00142008', '00000000000000000000000000000000'], ['0.00242', '00000000000000000010000000000000'], ['0.00242008', '00000000000000000000000000000000'], ['0.00262', '00000000000000000010000000000000'], ['0.00262008', '00000000000000000000000000000000'], ['0.00282', '00000000000000000010000000000000'], ['0.00282008', '00000000000000000000000000000000'], ['0.00332', '00000000000000000010000000000000'], ['0.00332008', '00000000000000000000000000000000'], ['0.00352', '00000000000000000010000000000000'], ['0.00352008', '00000000000000000000000000000000'], ['0.00372', '00000000000000000010000000000000'], ['0.00372008', '00000000000000000000000000000000'], ['0.00422', '00000000000000000010000000000000'], ['0.00422008', '00000000000000000000000000000000'], ['0.00442', '00000000000000000010000000000000'], ['0.00442008', '00000000000000000000000000000000'], ['0.00462', '00000000000000000010000000000000'], ['0.00462008', '00000000000000000000000000000000'], ['0.00512', '00000000000000000010000000000000'], ['0.00512008', '00000000000000000000000000000000'], ['0.00532', '00000000000000000010000000000000'], ['0.00532008', '00000000000000000000000000000000'], ['0.00552', '00000000000000000010000000000000'], ['0.00552008', '00000000000000000000000000000000'], ['0.00602', '00000000000000000010000000000000'], ['0.00602008', '00000000000000000000000000000000'], ['0.00622', '00000000000000000010000000000000'], ['0.00622008', '00000000000000000000000000000000'], ['0.00642', '00000000000000000010000000000000'], ['0.00642008', '00000000000000000000000000000000'], ['0.00692', '00000000000000000010000000000000'], ['0.00692008', '00000000000000000000000000000000'], ['0.00712', '00000000000000000010000000000000'], ['0.00712008', '00000000000000000000000000000000'], ['0.00732', '00000000000000000010000000000000'], ['0.00732008', '00000000000000000000000000000000'], ['0.00782', '00000000000000000010000000000000'], ['0.00782008', '00000000000000000000000000000000'], ['0.00802', '00000000000000000010000000000000'], ['0.00802008', '00000000000000000000000000000000'], ['0.00822', '00000000000000000010000000000000'], ['0.00822008', '00000000000000000000000000000000'], ['0.00872', '00000000000000000010000000000000'], ['0.00872008', '00000000000000000000000000000000'], ['0.00892', '00000000000000000010000000000000'], ['0.00892008', '00000000000000000000000000000000'], ['0.00912', '00000000000000000010000000000000'], ['0.00912008', '00000000000000000000000000000000'], ['0.00962', '00000000000000000010000000000000'], ['0.00962008', '00000000000000000000000000000000'], ['0.00982', '00000000000000000010000000000000'], ['0.00982008', '00000000000000000000000000000000'], ['0.01002', '00000000000000000010000000000000'], ['0.01002008', '00000000000000000000000000000000'], ['0.01003', '00000000000000000010000000000000'], ['0.01003008', '00000000000000000000000000000000'], ['0.01004', '00000000000000000010000000000000'], ['0.01004008', '00000000000000000000000000000000'], ['0.01005', '00000000000000000010000000000000'], ['0.01005008', '00000000000000000000000000000000'], ['0.01006', '00000000000000000010000000000000'], ['0.01006008', '00000000000000000000000000000000'], ['0.010066', '00000000000000000010000000000000'], ['0.01006608', '00000000000000000000000000000000'], ['0.010076', '00000100000000000010100000000000'], ['0.01007608', '00000100000000000000100000000000'], ['0.010176', '00000000000000000000100000000000'], ['0.013076', '00000000000000000010000000000000'], ['0.01307608', '00000000000000000000000000000000'], ['0.013176', '00000000000000000010000000000000'], ['0.01317608', '00000000000000000001000000000000'], ['0.01317616', '00000000000000000000000000000000'], ['0.0', '00000000000000000000000000000000']]
    print ttl == ttl_result
    for a,b in zip(ttl_result, ttl):
        if not a == b:
            print 'TTL Difference', a,b
    dds_result = [('global397', 0.0, -63.0), ('global397', 0.0, -63.0), ('global397', 89.99999987194315, -15.0), ('global397', 89.99999987194315, -15.0), ('global397', 89.99999987194315, -63.0), ('global397', 89.99999987194315, -63.0), ('global397', 89.99999987194315, -63.0), ('global397', 89.99999987194315, -63.0), ('global397', 89.99999987194315, -63.0), ('global397', 89.99999987194315, -63.0), ('global397', 89.99999987194315, -63.0), ('global397', 89.99999987194315, -63.0), ('global397', 89.99999987194315, -63.0), ('global397', 89.99999987194315, -63.0), ('global397', 89.99999987194315, -63.0), ('global397', 89.99999987194315, -63.0), ('global397', 89.99999987194315, -63.0), ('global397', 89.99999987194315, -63.0), ('global397', 89.99999987194315, -63.0), ('global397', 89.99999987194315, -63.0), ('global397', 89.99999987194315, -63.0), ('global397', 89.99999987194315, -63.0), ('global397', 89.99999987194315, -63.0), ('global397', 89.99999987194315, -63.0), ('global397', 89.99999987194315, -63.0), ('global397', 89.99999987194315, -63.0), ('global397', 89.99999987194315, -63.0), ('global397', 89.99999987194315, -63.0), ('global397', 89.99999987194315, -63.0), ('global397', 89.99999987194315, -63.0), ('global397', 89.99999987194315, -63.0), ('global397', 89.99999987194315, -63.0), ('global397', 89.99999987194315, -63.0), ('global397', 89.99999987194315, -63.0), ('global397', 89.99999987194315, -63.0), ('global397', 89.99999987194315, -63.0), ('global397', 89.99999987194315, -63.0), ('global397', 89.99999987194315, -63.0), ('global397', 89.99999987194315, -13.000457770656901), ('global397', 89.99999987194315, -63.0), ('global397', 89.99999987194315, -63.0), ('854DP', 0.0, -63.0), ('854DP', 0.0, -63.0), ('854DP', 79.99999990686774, -11.0), ('854DP', 79.99999990686774, -63.0), ('854DP', 79.99999990686774, -63.0), ('854DP', 79.99999990686774, -5.000457770656901), ('854DP', 79.99999990686774, -5.000457770656901), ('854DP', 79.99999990686774, -63.0), ('854DP', 79.99999990686774, -11.0), ('854DP', 79.99999990686774, -11.0), ('854DP', 79.99999990686774, -63.0), ('854DP', 79.99999990686774, -5.000457770656901), ('854DP', 79.99999990686774, -5.000457770656901), ('854DP', 79.99999990686774, -63.0), ('854DP', 79.99999990686774, -11.0), ('854DP', 79.99999990686774, -11.0), ('854DP', 79.99999990686774, -63.0), ('854DP', 79.99999990686774, -5.000457770656901), ('854DP', 79.99999990686774, -5.000457770656901), ('854DP', 79.99999990686774, -63.0), ('854DP', 79.99999990686774, -11.0), ('854DP', 79.99999990686774, -11.0), ('854DP', 79.99999990686774, -63.0), ('854DP', 79.99999990686774, -5.000457770656901), ('854DP', 79.99999990686774, -5.000457770656901), ('854DP', 79.99999990686774, -63.0), ('854DP', 79.99999990686774, -11.0), ('854DP', 79.99999990686774, -11.0), ('854DP', 79.99999990686774, -63.0), ('854DP', 79.99999990686774, -5.000457770656901), ('854DP', 79.99999990686774, -5.000457770656901), ('854DP', 79.99999990686774, -63.0), ('854DP', 79.99999990686774, -63.0), ('854DP', 79.99999990686774, -63.0), ('854DP', 79.99999990686774, -63.0), ('854DP', 79.99999990686774, -63.0), ('854DP', 79.99999990686774, -63.0), ('854DP', 79.99999990686774, -63.0), ('854DP', 79.99999990686774, -63.0), ('854DP', 79.99999990686774, -63.0), ('854DP', 79.99999990686774, -63.0), ('729DP', 0.0, -63.0), ('729DP', 0.0, -63.0), ('729DP', 0.0, -63.0), ('729DP', 0.0, -63.0), ('729DP', 0.0, -63.0), ('729DP', 219.99999997671694, -10.000228885328454), ('729DP', 219.99999997671694, -63.0), ('729DP', 219.99999997671694, -63.0), ('729DP', 224.99999986612238, -11.0), ('729DP', 224.99999986612238, -63.0), ('729DP', 224.99999986612238, -63.0), ('729DP', 219.99999997671694, -10.000228885328454), ('729DP', 219.99999997671694, -63.0), ('729DP', 219.99999997671694, -63.0), ('729DP', 224.99999986612238, -11.0), ('729DP', 224.99999986612238, -63.0), ('729DP', 224.99999986612238, -63.0), ('729DP', 219.99999997671694, -10.000228885328454), ('729DP', 219.99999997671694, -63.0), ('729DP', 219.99999997671694, -63.0), ('729DP', 224.99999986612238, -11.0), ('729DP', 224.99999986612238, -63.0), ('729DP', 224.99999986612238, -63.0), ('729DP', 219.99999997671694, -10.000228885328454), ('729DP', 219.99999997671694, -63.0), ('729DP', 219.99999997671694, -63.0), ('729DP', 224.99999986612238, -11.0), ('729DP', 224.99999986612238, -63.0), ('729DP', 224.99999986612238, -63.0), ('729DP', 219.99999997671694, -10.000228885328454), ('729DP', 219.99999997671694, -63.0), ('729DP', 219.99999997671694, -63.0), ('729DP', 219.99999997671694, -63.0), ('729DP', 219.99999997671694, -63.0), ('729DP', 219.99999997671694, -63.0), ('729DP', 219.99999997671694, -63.0), ('729DP', 214.99999990104698, -63.0), ('729DP', 214.99999990104698, -5.000457770656901), ('729DP', 214.99999990104698, -63.0), ('729DP', 214.99999990104698, -63.0), ('729DP', 214.99999990104698, -63.0), ('866DP', 0.0, -63.0), ('866DP', 0.0, -63.0), ('866DP', 79.99999990686774, -11.0), ('866DP', 79.99999990686774, -11.0), ('866DP', 79.99999990686774, -11.0), ('866DP', 79.99999990686774, -11.0), ('866DP', 79.99999990686774, -11.0), ('866DP', 79.99999990686774, -11.0), ('866DP', 79.99999990686774, -11.0), ('866DP', 79.99999990686774, -11.0), ('866DP', 79.99999990686774, -11.0), ('866DP', 79.99999990686774, -11.0), ('866DP', 79.99999990686774, -11.0), ('866DP', 79.99999990686774, -11.0), ('866DP', 79.99999990686774, -11.0), ('866DP', 79.99999990686774, -11.0), ('866DP', 79.99999990686774, -11.0), ('866DP', 79.99999990686774, -11.0), ('866DP', 79.99999990686774, -11.0), ('866DP', 79.99999990686774, -11.0), ('866DP', 79.99999990686774, -11.0), ('866DP', 79.99999990686774, -11.0), ('866DP', 79.99999990686774, -11.0), ('866DP', 79.99999990686774, -11.0), ('866DP', 79.99999990686774, -11.0), ('866DP', 79.99999990686774, -11.0), ('866DP', 79.99999990686774, -11.0), ('866DP', 79.99999990686774, -11.0), ('866DP', 79.99999990686774, -11.0), ('866DP', 79.99999990686774, -11.0), ('866DP', 79.99999990686774, -11.0), ('866DP', 79.99999990686774, -11.0), ('866DP', 79.99999990686774, -63.0), ('866DP', 79.99999990686774, -15.0), ('866DP', 79.99999990686774, -15.0), ('866DP', 79.99999990686774, -63.0), ('866DP', 79.99999990686774, -63.0), ('866DP', 79.99999990686774, -63.0), ('866DP', 79.99999990686774, -11.0), ('866DP', 79.99999990686774, -11.0), ('866DP', 79.99999990686774, -63.0), ('radial', 0.0, -63.0), ('radial', 0.0, -63.0), ('radial', 0.0, -63.0), ('radial', 0.0, -63.0), ('radial', 0.0, -63.0), ('radial', 0.0, -63.0), ('radial', 0.0, -63.0), ('radial', 0.0, -63.0), ('radial', 0.0, -63.0), ('radial', 0.0, -63.0), ('radial', 0.0, -63.0), ('radial', 0.0, -63.0), ('radial', 0.0, -63.0), ('radial', 0.0, -63.0), ('radial', 0.0, -63.0), ('radial', 0.0, -63.0), ('radial', 0.0, -63.0), ('radial', 0.0, -63.0), ('radial', 0.0, -63.0), ('radial', 0.0, -63.0), ('radial', 0.0, -63.0), ('radial', 0.0, -63.0), ('radial', 0.0, -63.0), ('radial', 0.0, -63.0), ('radial', 0.0, -63.0), ('radial', 0.0, -63.0), ('radial', 0.0, -63.0), ('radial', 0.0, -63.0), ('radial', 0.0, -63.0), ('radial', 0.0, -63.0), ('radial', 0.0, -63.0), ('radial', 0.0, -63.0), ('radial', 0.0, -63.0), ('radial', 99.99999983701855, -17.0004577706569), ('radial', 99.99999983701855, -63.0), ('radial', 99.99999983701855, -63.0), ('radial', 99.99999983701855, -63.0), ('radial', 99.99999983701855, -63.0), ('radial', 99.99999983701855, -63.0), ('radial', 99.99999983701855, -63.0), ('radial', 99.99999983701855, -63.0)]
    print dds == dds_result
    for a,b in zip(dds_result, dds):
        if not a == b:
            print 'DDS Difference', a,b
            
    readout = cxn.pulser.get_readout_counts().asarray
    print 'readout', readout
    channels = cxn.pulser.get_channels().asarray
    sp = SequencePlotter(ttl.asarray, dds.aslist, channels)
    sp.makePlot()