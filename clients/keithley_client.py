
import labrad
from time import *
from csv import *
import numpy as np
from keithley_helper import voltage_conversion as VC
from keithley_helper import resistance_conversion as RC

#Run on the Linux
cxnp = labrad.connect('192.168.169.29')
cxn = labrad.connect()
pulser = cxnp.pulser()
#Connect to Windows Computer to use Keithley DMM

#keithley = cxn.keithley_2110_dmm()
keithley = cxn.keithley_2110_dmm()

#keithley.select_device()
keithley2.select_device()
#load calibraton files and get ready for temperaturelookup
V529 = np.loadtxt('calibration files/529(Inside Heat Shield)_28062013_1107_keithley_DMM.csv',delimiter=',')
V529 = V529.transpose()
#C1 = np.loadtxt('calibration files/C1_28062013_1107_keithley_DMM.csv',delimiter=',')
#C1 = C1.transpose()
#C2 = np.loadtxt('calibration files/C2_28062013_1107_keithley_DMM.csv',delimiter=',')
#C2 = C2.transpose()
Cernox = np.loadtxt('calibration files/Cernox_28062013_1107_keithley_DMM.csv',delimiter=',')
Cernox = Cernox.transpose()
#TempC1 = np.interp(C1[0], V529[0], V529[3])
#TempC2 = np.interp(C2[0], V529[0], V529[3])
TempCernox = np.interp(Cernox[0], V529[0], V529[3])

#TempC1 = TempC1[::-1]
#TempC2 = TempC2[::-1]
TempCernox = TempCernox[::-1]
#VoltC1 = C1[2][::-1]
#VoltC2 = C2[2][::-1]
VoltCernox = Cernox[2][::-1]
TempV529=V529[3][::-1]
VoltV529=V529[2][::-1]

#Initially switch off the TTL pulse except the first one
pulser.switch_manual('Cold Finger', True)
pulser.switch_manual('Inside Heat Shield', False)
#pulser.switch_manual('C1', False)
#pulser.switch_manual('C2', False)
pulser.switch_manual('Cernox', False)

run_time = strftime("%d%m%Y_%H%M")
initial_time = time()
#BNC 526 is at Cold Finger
#filedirectory_526 = '/home/resonator/Desktop/Resonator_Voltage/526(Cold Finger)_'+run_time+'_keithley_DMM.csv'
filedirectory_526 = 'Y:/resonator-cooling/Data/resonator_auto/526(Cold Finger)_'+run_time+'_keithley_DMM.csv'
#BNC 529 is inside the heat shield
filedirectory_529 = 'Y:/resonator-cooling/Data/resonator_auto/529(Inside Heat Shield)_'+run_time+'_keithley_DMM.csv'
#
<<<<<<< HEAD
filedirectory_Cernox = 'Y:/resonator-cooling/Data/resonator_auto/Cernox_'+run_time+'_keithley_DMM.csv'
#
filedirectory_C1 = 'Y:/resonator-cooling/Data/resonator_auto/C1_'+run_time+'_keithley_DMM.csv'
#
filedirectory_C2 = 'Y:/resonator-cooling/Data/resonator_auto/C2_'+run_time+'_keithley_DMM.csv'
=======
filedirectory_Cernox = '/home/resonator/Desktop/Resonator_Voltage/Cernox_'+run_time+'_keithley_DMM.csv'
##
#filedirectory_C1 = '/home/resonator/Desktop/Resonator_Voltage/C1_'+run_time+'_keithley_DMM.csv'
##
#filedirectory_C2 = '/home/resonator/Desktop/Resonator_Voltage/C2_'+run_time+'_keithley_DMM.csv'
>>>>>>> e39d30f9439e8dd711b3b16b043c47a94588e7ed

# Each colum headers is the following:
#["Elapsed Time (minutes)", "CurrentTime(H:M)", "Voltage(V)", "Temperature(K)"

vc = VC()
rc = RC()
while(1):
<<<<<<< HEAD
#    pulser.switch_manual('Cold Finger', True)
=======
    pulser.switch_manual('Cold Finger', True)
    sleep(1)
>>>>>>> e39d30f9439e8dd711b3b16b043c47a94588e7ed
    file_526 = open(filedirectory_526,"ab")
    fcsv_526 = writer(file_526,lineterminator="\n")
    voltage = keithley2.get_dc_volts()
    temp = vc.conversion(voltage)
    elapsed_time_526 = (time() - initial_time)/60
    fcsv_526.writerow([round(elapsed_time_526,4), strftime("%H"+"%M"), voltage, round(temp, 3)])
    file_526.close()
    print voltage, temp
    pulser.switch_manual('Cold Finger', False)
    pulser.switch_manual('Inside Heat Shield', True)
<<<<<<< HEAD
    sleep(0.5)


#    file_C2 = open(filedirectory_C2,"ab")
#    fcsv_C2 = writer(file_C2,lineterminator="\n")
#    voltage = keithley2.get_dc_volts()
#    tempR=np.interp(voltage,VoltC1,TempC1)
=======
    sleep(2)
    
    file_529 = open(filedirectory_529,"ab")
    fcsv_529 = writer(file_529,lineterminator="\n")
    voltage = keithley.get_dc_volts()
    temp=vc.conversion(voltage)
    elapsed_time_529 = (time() - initial_time)/60
    fcsv_529.writerow([round(elapsed_time_529,4), strftime("%H"+"%M"), voltage, round(temp, 3)])
    file_529.close()
    print voltage, temp
    pulser.switch_manual('Inside Heat Shield', False)
    pulser.switch_manual('Cernox', True)
    sleep(20)

    file_Cernox = open(filedirectory_Cernox,"ab")
    fcsv_Cernox = writer(file_Cernox,lineterminator="\n")
    voltage = keithley.get_dc_volts()
    elapsed_time_Cernox = (time() - initial_time)/60
    TempCer = np.interp(voltage,VoltCernox,TempCernox)
    fcsv_Cernox.writerow([round(elapsed_time_Cernox, 4), strftime("%H"+"%M"), voltage, round(TempCer, 3)])
    file_Cernox.close()
    print voltage, TempCer
    pulser.switch_manual('Cernox', False)
    pulser.switch_manual('Cold Finger', True)
    sleep(20)
#    file_C1 = open(filedirectory_C1,"ab")
#    fcsv_C1 = writer(file_C1,lineterminator="\n")
#    voltage = keithley.get_dc_volts()
#    tempR=np.interp(voltage,VoltC1,TempC1)
#    elapsed_time_C1 = (time() - initial_time)/60
#    fcsv_C1.writerow([round(elapsed_time_C1,4), strftime("%H"+"%M"), voltage, round(tempR, 3)])
#    file_C1.close()
#    print tempR
#    pulser.switch_manual('C1', False)
#    pulser.switch_manual('C2', True)    
#    sleep(0.5)
#
#    file_C2 = open(filedirectory_C2,"ab")
#    fcsv_C2 = writer(file_C2,lineterminator="\n")
#    voltage = keithley.get_dc_volts()
#    tempR=np.interp(voltage,VoltC2,TempC2)
>>>>>>> e39d30f9439e8dd711b3b16b043c47a94588e7ed
#    elapsed_time_C2 = (time() - initial_time)/60
#    fcsv_C2.writerow([round(elapsed_time_C2,4), strftime("%H"+"%M"), voltage, round(tempR, 3)])
#    file_C2.close()
#    print tempR
<<<<<<< HEAD
#    # file_529 = open(filedirectory_529,"ab")
#    # fcsv_529 = writer(file_529,lineterminator="\n")
#    # voltage = keithley2.get_dc_volts()
#    # temp=vc.conversion(voltage)
#    # elapsed_time_529 = (time() - initial_time)/60
#    # fcsv_529.writerow([round(elapsed_time_529,4), strftime("%H"+"%M"), voltage, round(temp, 3)])
#    # file_529.close()
#    # print temp
#    pulser.switch_manual('Inside Heat Shield', False)
#    pulser.switch_manual('Cernox', True)
#    sleep(0.5)
#
#    file_Cernox = open(filedirectory_Cernox,"ab")
#    fcsv_Cernox = writer(file_Cernox,lineterminator="\n")
#    voltage = keithley2.get_dc_volts()
#    elapsed_time_Cernox = (time() - initial_time)/60
#    TempCer = np.interp(voltage,VoltCernox,TempCernox)
#    fcsv_Cernox.writerow([round(elapsed_time_Cernox, 4), strftime("%H"+"%M"), voltage, round(TempCer, 3)])
#    file_Cernox.close()
#    print TempCer
#    pulser.switch_manual('Cernox', False)
#    pulser.switch_manual('Cold Finger', True)
#    sleep(0.5)
    
##    file_C1 = open(filedirectory_C1,"ab")
##    fcsv_C1 = writer(file_C1,lineterminator="\n")
##    voltage = keithley.get_dc_volts()
##    tempR=np.interp(voltage,VoltC1,TempC1)
##    elapsed_time_C1 = (time() - initial_time)/60
##    fcsv_C1.writerow([round(elapsed_time_C1,4), strftime("%H"+"%M"), voltage, round(tempR, 3)])
##    file_C1.close()
##    print tempR
##    pulser.switch_manual('C1', False)
##    pulser.switch_manual('C2', True)    
##    sleep(0.5)
##
##    file_C2 = open(filedirectory_C2,"ab")
##    fcsv_C2 = writer(file_C2,lineterminator="\n")
##    voltage = keithley.get_dc_volts()
##    tempR=np.interp(voltage,VoltC2,TempC2)
##    elapsed_time_C2 = (time() - initial_time)/60
##    fcsv_C2.writerow([round(elapsed_time_C2,4), strftime("%H"+"%M"), voltage, round(tempR, 3)])
##    file_C2.close()
##    print tempR
##    pulser.switch_manual('C2', False)
##    pulser.switch_manual('Cold Finger', True)    
##    sleep(0.5)
=======
#    pulser.switch_manual('C2', False)
#    pulser.switch_manual('Cold Finger', True)    
#    sleep(0.5)
>>>>>>> e39d30f9439e8dd711b3b16b043c47a94588e7ed
    
    sleep(60)
