'''
Tool for general gapless plane approximation solutions
for planar traps.
'''

import numpy as np
from itertools import *
import matplotlib.pyplot as plt
import numdifftools as nd
        
#import numdifftools as nd
from analytic_derivatives import analytic_derivatives
from multipole_expansion import *

class Electrode():

    def __init__(self, location, derivatives):
        '''
        location is a 2-element list of the form
        [ (xmin, xmax), (ymin, ymax) ]

        axes_permutation is an integer.
        0 (default): normal surface trap. z-axis lies along the plane
        of the trap
        1: trap is in the x-y plane. z axis is vertical
        '''

        xmin, xmax = sorted(location[0])
        ymin, ymax = sorted(location[1])

        (self.x1, self.y1) = (xmin, ymin)
        (self.x2, self.y2) = (xmax, ymax)
        self.sub_electrodes = [] # list containing extra electrodes are connected to the current one

        self.multipole_expansion_dict = {} # keys are expansion points. elements are dictionaries of multipole expansions

        self.derivatives = derivatives

    def solid_angle(self, r):
        '''
        The solid angle for an arbitary rectangle oriented along the grid is calculated by
        Gotoh, et al, Nucl. Inst. Meth., 96, 3

        The solid angle is calculated from the current electrode, plus any additional electrodes
        that are electrically connected to the current electrode. This allows you to join electrodes
        on the trap, or to make more complicated electrode geometries than just rectangles.
        '''
        x, y, z = r
        solid_angle = self.derivatives['phi0'](self.x1, self.x2, self.y1, self.y2, x, y, z)

        for elec in self.sub_electrodes:
            solid_angle += elec.solid_angle(r)
        
        return solid_angle

    def grad(self, r):
        '''
        gradient of the solid angle at the observation point
        '''
        x, y, z = r
        keys = ['ddx', 'ddy', 'ddz']
        grad = np.array([self.derivatives[key](self.x1, self.x2, self.y1, self.y2, x, y, z)
                         for key in keys])
        for elec in self.sub_electrodes:
            grad += elec.grad(r)
        return grad

    def hessian(self, r):
        '''
        Hessian matrix at the observation point
        '''

        x, y, z = r
        hessian = np.zeros((3,3))
        
        hessian[0,0] = self.derivatives['d2dx2'](self.x1, self.x2, self.y1, self.y2, x, y, z)
        hessian[1,1] = self.derivatives['d2dy2'](self.x1, self.x2, self.y1, self.y2, x, y, z)
        hessian[2,2] = self.derivatives['d2dz2'](self.x1, self.x2, self.y1, self.y2, x, y, z)
        
        hessian[0,1] = hessian[1,0] = self.derivatives['d2dxdy'](self.x1, self.x2, self.y1, self.y2, x, y, z)
        hessian[0,2] = hessian[2, 0] = self.derivatives['d2dxdz'](self.x1, self.x2, self.y1, self.y2, x, y, z)
        hessian[1,2] = hessian[2,1] = self.derivatives['d2dydz'](self.x1, self.x2, self.y1, self.y2, x, y, z)

        for elec in self.sub_electrodes:
            hessian += elec.hessian(r)
        return  hessian

    def third_order_derivatives(self, r):
        '''
        We're not going to include all of them here, probably.
        '''
        keys = ['d3dz3', 'd3dxdz2','d3dydz2']
        x,y,z = r
        third_derivatives = np.array([self.derivatives[key](self.x1, self.x2, self.y1, self.y2, x, y, z)
                         for key in keys])
        for elec in self.sub_electrodes:
            third_derivatives += elec.third_order_derivatives(r)
        return third_derivatives

    def fourth_order_derivatives(self, r):
        keys = ['d4dz4', 'd4dx2dz2', 'd4dy2dz2']
        x, y, z = r
        fourth_derivatives = np.array([self.derivatives[key](self.x1, self.x2, self.y1, self.y2, x, y, z)
                         for key in keys])
        for elec in self.sub_electrodes:
            fourth_derivatives += elec.fourth_order_derivatives(r)
        return fourth_derivatives

    def extend(self, locations):
        '''
        Extend the current electrode by a set of rectangular regions
        '''
        for l in locations:
            elec = Electrode(l, self.derivatives)
            self.sub_electrodes.append(elec)

    def compute_potential(self, r):
        '''
        Compute potential at the observation point due only to this electrode. (That is,
        all other electrodes are grounded.)
        Is just the voltage on the electrode times the solid angle (over 2pi).
        Also since the charge is e, the potential energy due to this potential is already in eV
        '''

        return (self.voltage/(2*np.pi))*self.solid_angle(r)

    def compute_electric_field(self, r):
        '''
        Calculate the electric field at the observation point, given the voltage on the electrode
        If voltage is set in Volts, field is in Volts/meter.
        E = -grad(Potential)
        '''
        return -(self.voltage/2*np.pi)*self.grad(r)

    def compute_d_effective(self, r):
        '''
        Calculate the effective distance due to this electrode. This is defined
        as the parallel plate capacitor separation which gives the observed electric
        field for the given applied voltage. That is,
        Deff = V/E. Will be different in each direction so we return [deff_x, deff_y, deff_z]
        '''
        Ex, Ey, Ez = self.compute_electric_field(r)
        return [self.voltage/Ex, self.voltage/Ey, self.voltage/Ez] # in meters
        
    def set_voltage(self, v):
        self.voltage = v

    def expand_potential( self, r):
        '''
        Numerically expand the potential due to the electrode to second order as a taylor series
        around the obersvation point r = [x, y, z]

        self.taylor_dict is a dictionary containing the terms of the expansion. e.g.
        self.taylor_dict['x^2'] = (1/2)d^2\phi/dx^2
        '''
        # first set the voltage to 1V for this. Save the old voltage to restore at the end.
        try:
            old_voltage = self.voltage
            self.set_voltage(1.0)
        except:
            print "no old voltage set"

        self.taylor_dict = {}

        self.taylor_dict['r^0'] = self.compute_potential(r)

        grad = self.grad(r)
        self.taylor_dict['x'] = grad[0]
        self.taylor_dict['y'] = grad[1]
        self.taylor_dict['z'] = grad[2]

        '''
        Now compute the second derivatives
        '''
        hessian = self.hessian(r)
        self.taylor_dict['x^2'] = 0.5*hessian[0,0]
        self.taylor_dict['y^2'] = 0.5*hessian[1,1]
        self.taylor_dict['z^2'] = 0.5*hessian[2,2]
        self.taylor_dict['xy'] = hessian[0,1]
        self.taylor_dict['xz'] = hessian[0,2]
        self.taylor_dict['zy'] = hessian[1,2]

        # higher order stuff
        self.taylor_dict['z^3'], self.taylor_dict['xz^2'], self.taylor_dict['yz^2'] = self.third_order_derivatives(r)
        self.taylor_dict['z^4'], self.taylor_dict['x^2z^2'], self.taylor_dict['y^2z^2'] = self.fourth_order_derivatives(r)

        try:
            # now restore the old voltage
            self.set_voltage(old_voltage)
        except:
            print "no old voltage set"


    def expand_in_multipoles( self, r, r0 = 1):
        '''
        Obtain the multipole expansion for the potential due to the elctrode at the observation point.
        '''

        # first, make sure we have a taylor expansion of the potential
        self.expand_potential(r)
        self.multipole_dict = {}
        # multipoles
        self.multipole_dict['U1'] = (r0**2)*(2*self.taylor_dict['x^2'] + self.taylor_dict['z^2'])
        self.multipole_dict['U2'] = (r0**2)*(2 * self.taylor_dict['z^2'] - self.taylor_dict['x^2'] - self.taylor_dict['y^2'])
        self.multipole_dict['U3'] = 2*(r0**2)*self.taylor_dict['xy']
        self.multipole_dict['U4'] = 2*(r0**2)*self.taylor_dict['zy']
        self.multipole_dict['U5'] = 2*(r0**2)*self.taylor_dict['xz']

        # fields
        self.multipole_dict['Ex'] = -1*r0*self.taylor_dict['x']
        self.multipole_dict['Ey'] = -1*r0*self.taylor_dict['y']
        self.multipole_dict['Ez'] = -1*r0*self.taylor_dict['z']

        self.multipole_dict['r^0'] = self.taylor_dict['r^0']
        
        # stuff that isn't really multipoles

        self.multipole_dict['z^2'] = (r0)**2*2*self.taylor_dict['z^2']

        self.multipole_dict['z^4'] = (r0)**4*self.taylor_dict['z^4']/24.
        self.multipole_dict['xz^2'] = (r0)**3 * self.taylor_dict['xz^2']
        self.multipole_dict['yz^2'] = (r0)**3 * self.taylor_dict['yz^2']

        #These terms give corrections to (radial frequency)**2 along the z axis:
        self.multipole_dict['x^2z^2']  =  (r0)**4 * self.taylor_dict['x^2z^2']
        self.multipole_dict['y^2z^2']  =  (r0)**4 * self.taylor_dict['y^2z^2']


class World():
    '''
    Compute all electrodes
    '''
    def __init__(self, axes_permutation = 0):
        self.electrode_dict = {}
        self.rf_electrode_dict = {}
        self.dc_electrode_dict = {}

        if axes_permutation == 0:
            import ad_0 as ad
        if axes_permutation == 1:
            import ad_1 as ad
        self.derivatives = ad.functions_dict

    def add_electrode(self, name, xr, yr, kind, voltage = 0.0):
        '''
        Add an electrode to the World. Optionally set a voltage on it. Name it with a string.
        kind = 'rf' or 'dc'. If kind == 'rf', then add this electrode to the rf electrode dict
        as well as to the general electrode dict
        '''
        e = Electrode([xr, yr], self.derivatives)
        e.set_voltage(voltage)
        self.electrode_dict[name] = e
        
        if kind=='rf':
            self.rf_electrode_dict[name] = e
        if kind=='dc':
            self.dc_electrode_dict[name] = e

    def set_voltage(self, name, voltage):
        self.electrode_dict[name].set_voltage(voltage)

    def set_omega_rf(self, omega_rf):
        self.omega_rf = omega_rf

    def compute_total_dc_potential(self, r):
        v = 0
        for e in self.dc_electrode_dict.keys():
            el = self.electrode_dict[e]
            v += el.compute_potential(r)
        return v # the potential energy is automatically electron volts

    def compute_rf_field(self, r):

        '''
        Just add the electric field due to all the rf electrodes
        '''
        E = np.zeros(3)
        for name in self.rf_electrode_dict.keys():
            E += self.rf_electrode_dict[name].compute_electric_field(r)
        return E

    def compute_dc_field(self, r):
        E = np.zeros(3)
        for name in self.dc_electrode_dict.keys():
            E += self.dc_electrode_dict[name].compute_electric_field(r)
        return E
           

    def compute_squared_field_amplitude(self, r):
        Ex, Ey, Ez = self.compute_rf_field(r)
        
        return Ex**2 + Ey**2 + Ez**2 # has units of V^2/m^2

    def compute_pseudopot(self, r):
        q = 1.60217657e-19 # electron charge
        m = 6.64215568e-26 # 40 amu in kg
        omega_rf = self.omega_rf
        joule_to_ev = 6.24150934e18 # conversion factor to take joules -> eV
        E2 = self.compute_squared_field_amplitude(r)
        return (q**2/(4*m*omega_rf**2))*E2*joule_to_ev # psuedopotential in eV

    def compute_pseudopot_frequencies(self, r):
        '''
        This is only valid if xp, yp, zp is the trapping position. Return frequency (i.e. 2*pi*omega)
        '''
        ev_to_joule = 1.60217657e-19
        m = 6.64215568e-26 # 40 amu in kg
        hessdiag = nd.Hessdiag( self.compute_pseudopot )(r)
        
        d2Udx2 = ev_to_joule*hessdiag[0]
        d2Udy2 = ev_to_joule*hessdiag[1]
        d2Udz2 = ev_to_joule*hessdiag[2]
        '''
        Now d2Udx2 has units of J/m^2. Then w = sqrt(d2Udx2/(mass)) has units of angular frequency
        '''
        
        fx = np.sqrt(abs(d2Udx2)/m)/(2*np.pi)
        fy = np.sqrt(abs(d2Udy2)/m)/(2*np.pi)
        fz = np.sqrt(abs(d2Udz2)/m)/(2*np.pi)
        return [fx, fy, fz]

    def compute_dc_potential_frequencies(self, r):
        '''
        As always, this is valid only at the trapping position. Return frequency (not angular frequency)
        '''
        
        joule_to_ev = 6.24150934e18 # conversion factor to take joules -> eV
        ev_to_joule = 1.60217657e-19
        m = 6.64215568e-26 # 40 amu in kg
            
        H = nd.Hessian(self.compute_total_dc_potential)(r)   
        
        print H
        
        freq = np.linalg.eig(H)
        hessdiag = freq[0]
        eigvec = freq[1]

#        hessdiag = nd.Hessdiag( self.compute_total_dc_potential )(r)
        d2Udx2 = ev_to_joule*hessdiag[0]
        d2Udy2 = ev_to_joule*hessdiag[1]
        d2Udz2 = ev_to_joule*hessdiag[2]
        fx = np.sqrt(abs(d2Udx2)/m)/(2*np.pi)
        fy = np.sqrt(abs(d2Udy2)/m)/(2*np.pi)
        fz = np.sqrt(abs(d2Udz2)/m)/(2*np.pi)
        return [fx, fy, fz], eigvec

    def multipole_control_matrix(self, r, controlled_multipoles, r0 = 1, shorted_electrodes = []):
        elec_list = []
        for k in range(len(self.dc_electrode_dict.keys())):
            elname = str(k + 1)
            if elname not in shorted_electrodes:
                elec_list.append( self.dc_electrode_dict[elname] )
        print len(elec_list)
        me = MultipoleExpander(r, elec_list, controlled_multipoles, r0, compute_potentials = True)
        C = me.construct_control_matrix() # C does not contain the shorted electrodes
        print C
        # now add a row of zeros for each shorted electrode
        zerolist = np.zeros(len(controlled_multipoles))
        shorted_indices = [int(k) - 1 for k in shorted_electrodes]
        shorted_indices.sort() # needs to be in ascending order
        for i in shorted_indices:
            C = np.insert(C, i, zerolist, axis=1)
        return C

    def calculate_multipoles(self, multipole_list):
        multipoles = []
        
        for el in multipole_list:      
            m=0
            for elec in self.electrode_dict:
                #m += self.electrode_dict[elec].multipole_dict[el]
                m += self.electrode_dict[elec].multipole_dict[el]*self.electrode_dict[elec].voltage
            multipoles.append(m)
            
        return multipoles

    def drawTrap(self):
        import numpy as np
        import matplotlib.pyplot as plt
        import matplotlib.cm as cm
        plt.figure() #initialize figure
        
        def indiPlotter(elec,mycolor):
            import numpy
            import matplotlib.pyplot as plt
        
            xm=elec[0][0]*1e6
            xM=elec[0][1]*1e6
            ym=elec[1][0]*1e6
            yM=elec[1][1]*1e6
        
            #plot vertical lines
            plt.plot([xm,xm],[ym,yM],color=mycolor)
            plt.plot([xM,xM],[ym,yM],color=mycolor)
        
            #plot horizontal lines
            plt.plot([xm,xM],[ym,ym],color=mycolor)
            plt.plot([xm,xM],[yM,yM],color=mycolor)
        
        cmap = cm.get_cmap('Dark2')
        elec_colors = cmap(np.linspace(0,1,len(self.electrode_dict)))
        i=0
        for key in self.electrode_dict:
            myElec = self.electrode_dict[key]
            mycolor = elec_colors[i]
            indiPlotter([(myElec.x1,myElec.x2),(myElec.y1,myElec.y2)],mycolor) #plot each electrode
            for subelec in myElec.sub_electrodes:
                indiPlotter([(subelec.x1,subelec.x2),(subelec.y1,subelec.y2)],mycolor)
            i+=1
        
        orig_axes=plt.axis()
        new_axes=[0,0,0,0]
        
        #creating margins
        h_marg=1
        v_marg=1
        new_axes[0]=orig_axes[0]-h_marg
        new_axes[1]=orig_axes[1]+h_marg
        new_axes[2]=orig_axes[2]-v_marg
        new_axes[3]=orig_axes[3]-v_marg
                
        plt.axis(new_axes)
        plt.axes().set_aspect('equal')
        plt.xlabel('x (microns)')
        plt.ylabel('y (microns)')
        plt.show()
        
    
   


