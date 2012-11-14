class channelConfiguration(object):
    """
    Stores complete configuration for each of the channels
    """
    def __init__(self, channelNumber, ismanual, manualstate,  manualinversion, autoinversion):
        self.channelnumber = channelNumber
        self.ismanual = ismanual
        self.manualstate = manualstate
        self.manualinv = manualinversion
        self.autoinv = autoinversion
        
class ddsConfiguration(object):
    """
    Stores complete configuration of each DDS board
    """
    def __init__(self, address, allowedfreqrange, allowedamplrange, frequency, amplitude, **args):
        self.channelnumber = address
        self.allowedfreqrange = allowedfreqrange
        self.allowedamplrange = allowedamplrange
        self.frequency = frequency
        self.amplitude = amplitude
        self.state = True
        self.boardfreqrange = args.get('boardfreqrange', (0.0, 800.0))
        self.boardamplrange = args.get('boardamplrange', (-63.0, -3.0))
        self.boardphaserange = args.get('boardphaserange', (0.0, 360.0))
        self.off_parameters = args.get('off_parameters', (0.0, -63.0))
        self.remote = args.get('remote', False)        

class remoteChannel(object):
    def __init__(self, ip, server, reset, program):
        self.ip = ip
        self.server = server
        self.reset = reset
        self.program = program
        
class hardwareConfiguration(object):
    channelTotal = 32
    timeResolution = 40.0e-9 #seconds
    timeResolvedResolution = timeResolution/4.0
    maxSwitches = 1022
    isProgrammed = False
    sequenceType = None #none for not programmed, can be 'one' or 'infinite'
    collectionMode = 'Normal' #default PMT mode
    collectionTime = {'Normal':0.100,'Differential':0.100} #default counting rates
    okDeviceID = 'Pulser'
    okDeviceFile = 'photon.bit'
    
    #name: (channelNumber, ismanual, manualstate,  manualinversion, autoinversion)
    channelDict = {
		  '866':channelConfiguration(0, True, True, False, False),
                  'bluePI':channelConfiguration(1, False, True, False, False),
                  'adv':channelConfiguration(8, False, False, False, True),
                  'rst':channelConfiguration(9, False, False, False, True),
                  'wireVoltage':channelConfiguration(10, False, False, False, False),
                  '397sw':channelConfiguration(12, False, False, False, True),
                  '866sw':channelConfiguration(13, False, False, False, True),
<<<<<<< HEAD
                  '2W oven':channelConfiguration(14, False, False, False, True),
                  '854sw':channelConfiguration(15, False, False, False, False),
=======
                  '2W_oven':channelConfiguration(14, False, False, False, True),
>>>>>>> 5c2e272c4756243a45c82c446b47b7cbdb107402
                  #------------INTERNAL CHANNELS----------------------------------------#
                  'DiffCountTrigger':channelConfiguration(16, False, False, False, False),
                  'TimeResolvedCount':channelConfiguration(17, False, False, False, False),
                  'AdvanceDDS':channelConfiguration(18, False, False, False, False),
                  'ResetDDS':channelConfiguration(19, False, False, False, False)
                  }
    
    ddsDict = {
               '0':ddsConfiguration(0, (170.0,270.0),  (-63.0,-3.0), 220.0, -33.0)
#'1':ddsConfiguration(1, (170.0,270.0),  (-63.0,-3.0), 220.0, -33.0)
#'2':ddsConfiguration(2, (170.0,270.0),  (-63.0,-3.0), 220.0, -33.0),
#'3':ddsConfiguration(3, (170.0,270.0),  (-63.0,-3.0), 220.0, -33.0),
#'4':ddsConfiguration(4, (170.0,270.0),  (-63.0,-3.0), 220.0, -33.0)
#'5':ddsConfiguration(5, (170.0,270.0),  (-63.0,-3.0), 220.0, -33.0),
#'6':ddsConfiguration(6, (170.0,270.0),  (-63.0,-3.0), 220.0, -33.0),
#'7':ddsConfiguration(7, (170.0,270.0),  (-63.0,-3.0), 220.0, -33.0)
#               '397':ddsConfiguration(2, (170.0,270.0), (190.0,250.0), (-63.0,-3.0), (-63.0,-3.0), 220.0, -33.0),               
               #'729DP':ddsConfiguration(0, (190.0,250.0), (-63.0,-3.0), 220.0, -33.0, remote = 'pulser_729')
               }

    remoteChannels = {}#{ 'pulser_729': remoteChannel('192.168.169.49', 'pulser_729', 'reset_dds','program_dds')}
