import numpy as np

<<<<<<< Updated upstream
def generate_wavefunc(coupling_time, drive_frequ, Npoints=1000):
    """Creates a sine multiplied by a Gaussian given the parameters

    coupling_strength: in Hz
    drive_frequ: in Hz
    Npoints=1000
    """
    swap_time = float(coupling_time['s'])
    drive_frequ = float(drive_frequ["s"])
    exp_corr = 6 #Correction to keep the area constant
    t = np.linspace(0,swap_time * exp_corr,Npoints) - swap_time/2*exp_corr
    y = np.exp(-t**2/(swap_time**2))*np.sin(drive_frequ*2*np.pi*t)
    return t,y, 2*max(t)

def generate_wavefunc_blackman(coupling_time, drive_frequ, Npoints=1000):
    """Creates a sine multiplied by a Gaussian given the parameters

    coupling_strength: in Hz
    drive_frequ: in Hz
    Npoints=1000
    """
    coupling_time = float(coupling_time['s'])
    drive_frequ = float(drive_frequ["Hz"])
=======
def generate_wavefunc(coupling_time, detuning, Npoints=1000):
    """Creates a sine multiplied by a Gaussian given the parameters

    coupling_strength: in Hz
    detuning: in Hz
    Npoints=1000
    """
    swap_time = float(coupling_time)
    detuning = float(detuning)
    exp_corr = 6 #Correction to keep the area constant
    t = np.linspace(0,swap_time * exp_corr,Npoints) - swap_time/2*exp_corr
    y = np.exp(-t**2/(swap_time**2))*np.sin(detuning*2*np.pi*t)
    return t,y, 2*max(t)

def generate_wavefunc_blackman(coupling_time, detuning, Npoints=1000):
    """Creates a sine multiplied by a Gaussian given the parameters

    coupling_strength: in Hz
    detuning: in Hz
    Npoints=1000
    """
    coupling_time = float(coupling_time)
    detuning = float(detuning)
>>>>>>> Stashed changes
    exp_corr = 1/.42 #Correction to keep the area constant
    t = np.linspace(0,coupling_time * exp_corr,Npoints)# - swap_time/2*exp_corr
    t0 = coupling_time * exp_corr
    alph = .16
    a = [(1-alph)/2.0, 1/2., alph/2.]
    y_blackman = a[0] - a[1] * np.cos(2*np.pi*t/t0) +  a[2] * np.cos(4*np.pi*t/t0) 
<<<<<<< Updated upstream
    y = y_blackman *np.sin(drive_frequ*2*np.pi*t)
=======
    y = y_blackman *np.sin(detuning*2*np.pi*t)
>>>>>>> Stashed changes
    print max(t)
    return t,y, max(t)
            
def to_str(y):
    s1 = ''
    for i in y:
        s1 += str(i) +', '
    return s1.strip(', ')

<<<<<<< Updated upstream
def write_to_agilent(coupling_time,drive_frequ,amplitude,Npoints=10000, is_black=True):
    """Writes the wavefunction directly to the generator
    coupling_strength in Hz
    drive_frequ in Hz
    amplitude in dBm
    """
    if is_black:
        t,y,duration = generate_wavefunc_blackman(coupling_time,drive_frequ,Npoints)
    else:
        t,y,duration = generate_wavefunc(coupling_time,drive_frequ,Npoints)
=======
def write_to_agilent(coupling_time,detuning,amplitude,Npoints=10000, is_black=True):
    """Writes the wavefunction directly to the generator
    coupling_strength in Hz
    detuning in Hz
    amplitude in dBm
    """
    if is_black:
        t,y,duration = generate_wavefunc_blackman(coupling_time,detuning,Npoints)
    else:
        t,y,duration = generate_wavefunc(coupling_time,detuning,Npoints)
>>>>>>> Stashed changes
    s1 = to_str(y)
    freq = 1/duration
    import labrad
    from labrad.units import WithUnit
    cxn = labrad.connect('192.168.169.30')
    a = cxn.agilent_server
    a.select_device()
    a.output(False)
    a.arbitrary_waveform2(s1)
    a.output(True)
    a.amplitude(WithUnit(amplitude,'dBm'))
    a.frequency(WithUnit(freq,'Hz'))
    print freq

<<<<<<< Updated upstream
def write_to_rigol(coupling_time,drive_frequ,amplitude1,amplitude2,Npoints=100000, is_black=True):
    """Writes the wavefunction directly to the generator
    coupling_strength in Hz
    drive_frequ in Hz
    amplitude in dBm
    """
    if is_black:
        t,y,duration = generate_wavefunc_blackman(coupling_time,drive_frequ,Npoints)
    else:
        t,y,duration = generate_wavefunc(coupling_time,drive_frequ,Npoints)
=======
def write_to_rigol(coupling_time,detuning,amplitude1,amplitude2,Npoints=100000, is_black=True):
    """Writes the wavefunction directly to the generator
    coupling_strength in Hz
    detuning in Hz
    amplitude in dBm
    """
    if is_black:
        t,y,duration = generate_wavefunc_blackman(coupling_time,detuning,Npoints)
    else:
        t,y,duration = generate_wavefunc(coupling_time,detuning,Npoints)
>>>>>>> Stashed changes
    s1 = to_str(y)
    freq = 1/duration
    import labrad
    from labrad.units import WithUnit
    cxn = labrad.connect('192.168.169.30')
    a = cxn.rigol_dg4062_server
    a.select_device()
    #Set channel 1
    a.burst_state(True,1)
    a.arbitrary_waveform(s1,1)
    a.voltage(WithUnit(amplitude1,'V'),1)
    a.frequency(WithUnit(freq,'Hz'),1)

    #Set channel 2
    a.burst_state(True,2)
    a.arbitrary_waveform(s1,2)
    a.frequency(WithUnit(freq,'Hz'),2)
    a.voltage(WithUnit(amplitude2,'V'),2)
    a.burst_state(True,2)
    a.burst_state(True,1)
    print freq


if __name__ == "__main__":
<<<<<<< Updated upstream
#    t,y,duration = generate_wavefunc(8e3, 133e3)
#    freq= 1/duration
    from labrad.units import WithUnit
    coupling_time = WithUnit(3e-4,'s')
    drive_frequ = WithUnit(1.695,'MHz')
    amplitude = 13
    amplitude2 = 1.0
#    write_to_rigol(coupling_strength,drive_frequ,amplitude,amplitude2)
    write_to_agilent(coupling_time,drive_frequ,amplitude,is_black=True,Npoints=50000)
=======
    t,y,duration = generate_wavefunc(8e3, 133e3)
    freq= 1/duration
    coupling_time = 3e-4
    detuning = 1.695e6
    amplitude = 13
    amplitude2 = 1.0
#    write_to_rigol(coupling_strength,detuning,amplitude,amplitude2)
    write_to_agilent(coupling_time,detuning,amplitude,is_black=True,Npoints=50000)
>>>>>>> Stashed changes
