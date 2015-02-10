import numpy as np
import lmfit
import camera_pmt as cpmt

class ion_state_detector(object):
    """1D ion state detector: Should only be used with horizontal ion strings"""
    def __init__(self, ion_positions, model_threshold = 0.1):
        """1D ion state detector: Should only be used with horizontal ion strings
        ion_positions: array of ion x positions
        model_threshold: float threshold determining the range over with the chi^2 is calculated
        """
        self.ion_number = len(ion_positions)
        self.all_state_combinations = self.all_combinations_0_1(self.ion_number)
        self.ion_positions = ion_positions
        self.model_threshold = model_threshold
        self.fitted_gaussians_1d, self.background = None, None
    
    def set_fitted_parameters(self, params, xx, yy):       
        self.fitted_gaussians_1d = self.ion_gaussians(params, xx, yy, use_1d=True)
        self.allions_1d = (self.ion_model(params, xx, yy, use_1d=True) - params['background_level'].value) \
                          / params['amplitude'].value
        self.background = params['background_level'].value
        self.params = params
        self.xx = xx
        self.yy = yy

    def gaussian_1D(self, xx, x_center, sigma_x, amplitude):
        '''xx is the provided meshgrid of x generates a 1D gaussian for
        centered at x_center
        '''
        xx = xx[0,:]
        result =  amplitude * np.exp( - (xx - x_center)**2 / (2 * sigma_x**2))
        return result


    def gaussian_2D(self, xx, yy, x_center, y_center, sigma_x, sigma_y, amplitude):
        '''
        xx and yy are the provided meshgrid of x and y coordinates
        generates a 2D gaussian for centered at x_center and y_center
        '''
        result = amplitude * np.exp( - (xx - x_center)**2 / (2 * sigma_x**2)) *  np.exp( - (yy - y_center)**2 / (2 * sigma_y**2))
        return result
    
    def ion_gaussians(self, params, xx, yy, use_1d=True):
        '''
        N is params['ion_number']
        
        returns a (N-long) array where i-th element corresponds to the gaussian centered at the i-th ion.
        '''
        if use_1d:
            ion_gaussians  = np.empty((self.ion_number, xx.shape[1]))
        else:
            ion_gaussians  = np.empty((self.ion_number, xx.shape[0], xx.shape[1]))
        position_list = []
        #lmfit cannot handle an array of parameters so here we go
        try:
            i = 0
            while(True):
                position_list.append(params['pos'+str(i)].value)
                i += 1
        except KeyError:
            pass
        amplitude = params['amplitude'].value #all ions are assumsed to have the same amplitude
        sigma = params['sigma'].value #width along the axis
        for i in range(self.ion_number):
            if use_1d:
                ion_gaussians[i] = self.gaussian_1D(xx,  self.ion_positions[i], 
                                                     sigma, amplitude)
            else:
                raise NotImplementedError("Cannot do 2 dimensional fit anymore - Sorry")
        return ion_gaussians
  
    def ion_model(self, params, xx, yy, use_1d=True):
        '''
        calcultes the sum of the background and all the gaussians centered at every ion
        '''
        summed_gaussians = params['background_level'].value + self.ion_gaussians(params, xx, yy, 
                                                                                 use_1d=use_1d).sum(axis = 0)
        return summed_gaussians


    def cartesian_product(self, arrays):
        '''
        http://stackoverflow.com/questions/1208118/using-numpy-to-build-an-array-of-all-combinations-of-two-arrays
        '''
        broadcastable = np.ix_(*arrays)
        broadcasted = np.broadcast_arrays(*broadcastable)
        rows, cols = reduce(np.multiply, broadcasted[0].shape), len(broadcasted)
        out = np.empty(rows * cols, dtype=broadcasted[0].dtype)
        start, end = 0, rows
        for a in broadcasted:
            out[start:end] = a.reshape(-1)
            start, end = end, end + rows
        return out.reshape(cols, rows).T
    
    def all_combinations_0_1(self, n):
        '''
        create all comibations of  (0) and (1)
        
        i.e
        
        2 -> [[0,0],[0,1],[1,0],[1,1]]
        3 -> [[0,0,0],[0,0,1],...,[1,1,1]]
        '''
        return self.cartesian_product([[0,1] for i in range(n)])
    
    def fitting_error(self, params , xx, yy,  data):
        data = data.sum(axis=0)
        data = data - data[0]
        model = self.ion_model(params, xx, yy)
        scaled_difference = (model - data) #/ np.sqrt(data)
        position_list = []
        try:
            i = 0
            while(True):
                position_list.append(params['pos'+str(i)].value)
                i += 1
        except KeyError:
            pass
        use_x = np.zeros_like(data)
        for position in position_list:
            use_x += np.abs(xx[0,:] - position) < params['sigma'] * 2

        scaled_difference = scaled_difference * use_x
        return scaled_difference.ravel()
    
    def fitting_error_state(self, selection, image):
        '''
        '''
        sum_selected_gaussians =  np.tensordot(selection, self.fitted_gaussians_1d, axes = (1, 0))
        sum_selected_gaussians = sum_selected_gaussians[:, None, :]
        image_size = float(image.shape[1] * image.shape[2]) 
        image = image.sum(1)

        image = image - image[:,0].mean() #Remove background

        a1d = np.ones_like(self.allions_1d)
        low_values_indices = self.allions_1d < self.model_threshold  # Where values are low
        a1d[low_values_indices] = 0  # All low values set to 0
        weight = a1d[None, None, :]

        chi_sq = (sum_selected_gaussians - image)**2 * weight / image_size
        #chi_sq = (sum_selected_gaussians - image)**2 / image_size
        chi_sq = chi_sq.sum(axis = 2) 
        best_states = selection[np.argmin(chi_sq, axis = 0)]
        sorted_chi = np.sort(chi_sq, axis = 0)
        lowest_chi,second_lowest_chi = sorted_chi[0:2]
        confidence = 1 - lowest_chi / second_lowest_chi
        return best_states, confidence

    def guess_parameters_and_fit(self, xx, yy, data):
        print 'Max data', np.max(data)
        params = lmfit.Parameters() 
        #background_guesse = np.sum(data[:,0]) #assumes that there are no ions at the edge of the image
        background_guess = 0
        amplitude_guess = np.sum(data[:,self.ion_positions[0]-np.min(xx)]) - np.sum(data[:,0])
        print 'ampl ', amplitude_guess
        sigma_guess = 3 #assume it's hard to resolve the ion, sigma ~ 1
        params.add('background_level', value = background_guess, min = 0.0, vary=True)
        params.add('amplitude', value = amplitude_guess, min = 0.0, vary=True)
        params.add('sigma', value = sigma_guess, min = 0.01, max = 10.0, vary=True)
        for [i, position] in enumerate(self.ion_positions):
            pname = 'pos' + str(i)
            params.add(pname, value=position, vary=True)
        result = lmfit.minimize(self.fitting_error, params, args = (xx, yy, data))
        print result.params
        self.set_fitted_parameters(params, xx, yy)
        return result, params
        
        
    def state_detection(self, image, pmt_mode=False):
        '''
        given the image and the parameters of the reference images with all ions bright, determines
        which ions are currently darks
        '''
        if self.fitted_gaussians_1d is None:
            raise Exception("Fitted parameters not provided")
        if image.ndim == 2:
            #if only a single image is provided, shape it to be a 1-long sequence
            image = image.reshape((1, image.shape[0],image.shape[1]))
        if pmt_mode == True:
            raise NotImplementedError('PMT mode is not supported anymore')

        state, confidence = self.fitting_error_state(self.all_state_combinations, image)
        return state, confidence

    def report(self, params):
        lmfit.report_errors(params)
    
    def graph(self, x_axis, y_axis, image, params, result = None):
        #plot the sample data
        from matplotlib import pyplot
        pyplot.figure()
        pyplot.subplot(2,1,1)
        pyplot.contourf(x_axis, y_axis, image, alpha = 0.5)
        #plot the fit
        #sample the fit with more precision

        x_axis_fit = np.linspace(x_axis.min(), x_axis.max(), x_axis.size * 5)
        y_axis_fit = np.linspace(y_axis.min(), y_axis.max(), y_axis.size * 5)
        xx, yy = np.meshgrid(x_axis_fit, y_axis_fit)
        params['background_level'].value = 0                                                                                
        fit_1d = self.ion_model(params, xx, yy, use_1d=True)
        xx, yy = np.meshgrid(x_axis, y_axis)
        pyplot.subplot(2,1,2)
        ximage = image.sum(axis=0)
        ximage = ximage - ximage[0]
        a1d = np.ones_like(self.allions_1d)
        #low_values_indices = self.allions_1d - bg < (0.5)*params['amplitude'].value  # Where values are low
        low_values_indices = self.allions_1d < self.model_threshold  # Where values are low
        a1d[low_values_indices] = 0  # All low values set to 0
        pyplot.plot(x_axis, a1d * ximage.max())
        #pyplot.plot(x_axis, ximage * a1d, 'o', markersize=10)
        pyplot.plot(x_axis, ximage)
        pyplot.plot(x_axis_fit, fit_1d)
        pyplot.tight_layout()
        pyplot.show()
#        import IPython as ip
#        ip.embed()
