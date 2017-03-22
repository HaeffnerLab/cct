'''
Gapless approximation code. Refers to the cct Abashiri trap.
'''

import csv

try:
    from gapless import World
except:
    from trapsim.gapless import World

import numpy as np
import matplotlib.pyplot as plt

'''
Add all the electrodes electrodes
'''
point_trap = 1 #boolean if point trap or not



if point_trap == 1:
    shorts = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16']
else: 
    shorts = ['9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25']
    shorts2 = ['1','2','3','4','5','6','7','8','17','18','19','20','21','22','23','24','25']

#double trap
edim = 150.0e-6 #dimensions of electrodes
ht = 150.0e-6
hb = 200.0e-6
l1=50.0e-6
l2=90.0e-6
r = edim/2.
x_ranges1 = (-r,0)
y_ranges1 = (r,r+ht)
x_ranges2 = (0,r)
y_ranges2 = (r,r+ht)
x_ranges3 = (-r-l1-l2,-r-l1)
y_ranges3 = (-r,r)
x_ranges4 = (-r-l1,-r)
y_ranges4 = (-r,r)
x_ranges5 = (r,r+l1)
y_ranges5 = (-r,r)
x_ranges6 = (r+l1,r+l1+l2)
y_ranges6 = (-r,r)
x_ranges7 = (-r,0)
y_ranges7 = (-r,-r-hb)
x_ranges8 = (0,r)
y_ranges8 = (-r,-r-hb)


x_ranges = [x_ranges1,x_ranges2,x_ranges3,x_ranges4,x_ranges5,x_ranges6,x_ranges7,x_ranges8]
y_ranges = [y_ranges1,y_ranges2,y_ranges3,y_ranges4,y_ranges5,y_ranges6,y_ranges7,y_ranges8]
 
y_ranges2 = []
y_ranges2[:] = [(-y1,-y2) for (y1,y2) in y_ranges]
x_ranges.extend(x_ranges)
y_ranges.extend(y_ranges2)

# single trap
edim = 270.0e-6 #dimensions of electrodes
ht = 520.0e-6
hb = 520.0e-6
l1=130.0e-6
l2=160.0e-6
r = edim/2.
x_ranges1 = (-r,0)
y_ranges1 = (r,r+ht)
x_ranges2 = (0,r)
y_ranges2 = (r,r+ht)
x_ranges3 = (-r-l1-l2,-r-l1)
y_ranges3 = (-r,r)
x_ranges4 = (-r-l1,-r)
y_ranges4 = (-r,r)
x_ranges5 = (r,r+l1)
y_ranges5 = (-r,r)
x_ranges6 = (r+l1,r+l1+l2)
y_ranges6 = (-r,r)
x_ranges7 = (-r,0)
y_ranges7 = (-r,-r-hb)
x_ranges8 = (0,r)
y_ranges8 = (-r,-r-hb)
x_ranges9 = (-r,r) 
y_ranges9 = (-r,r)

x_ranges.extend([x_ranges1,x_ranges2,x_ranges3,x_ranges4,x_ranges5,x_ranges6,x_ranges7,x_ranges8,x_ranges9])
y_ranges.extend([y_ranges1,y_ranges2,y_ranges3,y_ranges4,y_ranges5,y_ranges6,y_ranges7,y_ranges8,y_ranges9])


''' Now build your own world '''
w = World(1)
# first build the dc electrodes
i=0
r = [0,0,120e-6]

for xr, yr in zip(x_ranges, y_ranges):
    i=i+1
    w.add_electrode(str(i), xr, yr, 'dc')
    #for xrp, yrp in zip(xlist[i-1], ylist[i-1]):
    #        w.dc_electrode_dict[str(i)].extend( [[ xrp,yrp ]] )    
    w.dc_electrode_dict[str(i)].expand_in_multipoles(r)

C1 = w.multipole_control_matrix(r,['Ex','Ey','Ez','U1','U3'], r0=1e-3,shorted_electrodes = shorts) #compute the control matrix for section
if point_trap == 0:
    C2 = w.multipole_control_matrix(r,['Ex','Ey','Ez','U1','U3'], r0=1e-3,shorted_electrodes = shorts2)
    C = np.append(C1,C2,axis=0)
else: 
    C = C1
       
#write control matrix to file
f=open('Abashiri_CMartix.csv','w')
for i in range(0,len(C[:,1])):
    np.savetxt(f, C[i,:], delimiter=",")
f.close()


#set electrode voltages to study potential frequencies from DC electrodes
#for elname in range(1,9):
    
    #w.set_voltage(str(elname),C[3,elname-1])
    #print(w.electrode_dict[str(elname)].voltage)


#w.set_voltage(str(1),.911)
#w.set_voltage(str(2),.449)
#w.set_voltage(str(3),0)
#w.set_voltage(str(4),-4.33)
#w.set_voltage(str(5),5.961)
#w.set_voltage(str(6),0)
#w.set_voltage(str(7),-3.32)
#w.set_voltage(str(8),0)

#values = w.calculate_multipoles(['Ex','Ey','Ez','U1','U3'])

#print values

#print ''

#omegax=[]
#omegay=[]
#omegaz=[]
#for el in omega:
#    omegax.append(el[0])
#    omegay.append(el[1])
#    omegaz.append(el[2])
#
#plt.plot(l,omegax,'ro',l,omegay,'bs',l,omegaz,'g^')
#plt.show(block = True)
#
#m = w.calculate_multipoles(['Ex','Ey','Ez','U1','U2','U3','U4','U5'])
#print 'Multipoles = '
#print m
print C

#draw the trap
w.drawTrap()



