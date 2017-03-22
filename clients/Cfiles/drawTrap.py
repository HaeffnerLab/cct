def drawTrap(self):
    #electrodes is a dictionary with names as keys and electrode objects as values
    import numpy as np
    import matplotlib.pyplot as plt
    plt.figure() #initialize figure
    for key in self.electrode_dict:
        myElec = electrode_dict[key]
        indiPlotter([(myElec.x1,myElec.x2),(myElec.y1,myElec.y2)]) #plot each electrode
    
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
    
    def indiPlotter(elec):
        import numpy
        import matplotlib.pyplot as plt
    
        xm=elec[0][0]*1e6
        xM=elec[0][1]*1e6
        ym=elec[1][0]*1e6
        yM=elec[1][1]*1e6
    
        #plot vertical lines
        plt.plot([xm,xm],[ym,yM],color='black')
        plt.plot([xM,xM],[ym,yM],color='black')
    
        #plot horizontal lines
        plt.plot([xm,xM],[ym,ym],color='black')
        plt.plot([xm,xM],[yM,yM],color='black')
   
