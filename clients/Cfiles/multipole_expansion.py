'''
Find out how to set each electrode such that we acheive the desired
multipole expansion of the total potential
'''

import numpy as np

class MultipoleExpander():

    def __init__(self, r, li, controlled_multipoles, r0 = 1, compute_potentials = True):
        '''
        Specify the expansion point, and the list
        of electrodes that should appear in the 
        multipole control array. The list must
        be in the order that you would like the electrodes
        to appear in the control file.

        controlled_multipoles is a list of names of the multipoles
        to appear in the control matrix. It should be in the order
        in which the multipoles should appear in the control file.
        r0 sets the units of the multipole coefficients
        compute_potentials = True makes the MultipoleExpander
        compute the electrode potentials at the point. Set to false
        if they have already been computed elsewhere.
        '''
        self.r = r
        self.electrode_list = li
        self.controlled_multipoles = controlled_multipoles
        if compute_potentials:
            for elec in li:
                elec.expand_in_multipoles(r, r0)

    
    def construct_inverse_matrix(self):
        '''
        This is the matrix we already have. It maps
        the voltages on each electrode to the total multipole
        configuration
        '''
        multipole_arr = np.zeros( ( len(self.electrode_list), len(self.controlled_multipoles)) )
        for i, elec in enumerate(self.electrode_list):
            multipole_arr[i,:] = [elec.multipole_dict[multipole] for multipole in self.controlled_multipoles]

        self.multipole_arr = multipole_arr

    
    def construct_control_matrix(self):
        '''
        Construct the multipole control matrix
        '''

        self.construct_inverse_matrix()

        C = []
        n_mult = len(self.controlled_multipoles)
        for mult in range(n_mult):
            B = np.zeros(n_mult)
            B[mult] = 1
            A = np.linalg.lstsq(self.multipole_arr.transpose(), B)[0]
            C.append(A)
        C = np.array(C)
        self.C = C
        return C
