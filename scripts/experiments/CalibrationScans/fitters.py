from scipy.optimize import curve_fit
import numpy as np
import matplotlib.pyplot as plt
import lmfit

class pi_time_fitter():

    def guess_tpi(self, t, exci):
        '''
        Start from the beginning of the flop.
        Use the starting guess as the first time
        the flop value goes down AND the flop has
        exceeded 0.9 excitation probability.
        '''

        last = 0
        for i, ex in enumerate(exci):
            if ex < last and last >= 0.9: return t[i-1]
            last = ex
        raise Exception('No valid pi time guess')

    def fit(self, t, exci):
        t0 = self.guess_tpi(t, exci)
        model = lambda x, tpi: np.sin(np.pi/2/tpi*np.array(x))**2
        t_pi, c = curve_fit(model, t, exci, p0 = t0)
        return t_pi[0]

class peak_fitter():
    
    def guess(self, f, p, force_guess = False):
        '''
        just take the point at the peak value
        '''
        max_index = np.where(p == p.max())[0][0]
        fmax = f[max_index]
        if (p.max() <= 0.2 and not force_guess):
            raise Exception("Peak not found")
        else:
            # center, amplitude, width guesses
            return np.array([ fmax,  p.max(), 6e-3 ])
    
    def fit(self, f, p, return_all_params = False):
        model = lambda x, c0, a, w: a*np.exp(-(x - c0)**2/w**2)
        force_guess = False
        if return_all_params: force_guess = True
        guess = self.guess(f, p, force_guess)
        popt, copt = curve_fit(model, f, p, p0=guess)
        if return_all_params:
            return popt[0], popt[1], popt[2] # center value, amplitude, width
        else:
            return popt[0] # return only the center value


def print_result(result):

    for k in result.var_names:
       print(k + " = " + str(result.params[k].value))

class scat_rate_fitter():
 
    def fcn2min(self, params, x, data, return_fit = False):
        """ model decaying sine wave, subtract data"""
        A = params['A'].value
        alpha = params['alpha'].value
        delta = params['delta'].value
    
        self.gamma = 21.87
        #model = A*2*alpha*(x/gamma**2)/(1+(2*alpha*x/gamma**2)+4*(delta/gamma)**2)
        model = A * alpha/(1 + alpha + 4*(x - delta)**2/self.gamma**2)

        if return_fit:
            return model
        else:
            return model - data
   
    def guess(self, counts):
        return 424.0, 0.2, max(counts)
    
    def fit(self, freq, counts, spec_time = 400.0): 
        guess = self.guess(counts)

        A_calib = 8.5/400.0

        # create a set of Parameters
        params = lmfit.Parameters()
        params.add('delta', value = guess[0], min = 400.0, max = 560.0, vary = True)
        params.add('alpha', value = guess[1], min = 0.1, max = 10.0, vary = True)
        params.add('A', value = spec_time * A_calib, vary = False)

        x = freq
        y = counts
        minner = lmfit.Minimizer(self.fcn2min, params, fcn_args=(x, y))
        result = minner.minimize()

        alpha_fit = result.params['alpha'].value
        delta_fit = result.params['delta'].value
        A_fit = result.params['A'].value

        print alpha_fit
        print delta_fit
        print A_fit

        rabi_freq = np.sqrt(alpha_fit * self.gamma**2 / 2.0) #in MHz



        plt.plot(freq, self.fcn2min(result.params, freq, None, return_fit = True))
        plt.plot(freq, counts, 'ko')
        xpos = .1*(max(x)-min(x)) + min(x)
        ypos = .8*(max(y)-min(y)) + min(y)
        plt.annotate('Rabi Frequency \n in MHz = ' + str(rabi_freq), xy = (xpos, ypos), xytext = (xpos, ypos))
        plt.xlabel('Real Frequency (MHz)')
        plt.ylabel('kCounts')
        plt.show()

        return rabi_freq

class old_old_scat_rate_fitter():
 
    def fcn2min(self, params, x, data, return_fit = False):
        """ model decaying sine wave, subtract data"""
        A = params['A'].value
        alpha = params['alpha'].value
        delta = params['delta'].value
    
        gamma = 2*np.pi*21.87e6
        model = A*2*alpha*(x/gamma**2)/(1+(2*alpha*x/gamma**2)+4*(delta/gamma)**2)

        if return_fit:
            return model
        else:
            return model - data
   
    def guess(self,counts):
        return 2*np.pi*22.0e6, 5.0e20, max(counts)
    
    def fit(self, PAO_log, counts):        
        PAO = 1.0e-3*10.0**(PAO_log/10.0)#b/c AOM power is in dBm

        guess = self.guess(counts)

        # create a set of Parameters
        params = lmfit.Parameters()
        params.add('delta', value = guess[0], min = 2*np.pi*10.0e6, max = 2*np.pi*100e6, vary = True)
        params.add('alpha', value = guess[1], min = 1e19, max = 1e21, vary = True)
        params.add('A', value = guess[2], min = 70.0, vary = True)

        x = PAO
        y = counts
        minner = lmfit.Minimizer(self.fcn2min, params, fcn_args=(x, y))
        result = minner.minimize()

        alpha_fit = result.params['alpha'].value
        delta_fit = result.params['delta'].value
        A_fit = result.params['A'].value

        print alpha_fit
        print delta_fit/2/np.pi/1e6
        print A_fit

        plt.plot(PAO_log, self.fcn2min(result.params, PAO, None, return_fit = True))
        plt.plot(PAO_log, counts, 'ko')
        plt.show()

        return alpha_fit

class old_scat_rate_fitter():
    
    def guess(self,counts):
        return 2*np.pi*20.0e6, 1.0e20, max(counts)
    
    def fit(self, PAO_log, counts):
        PAO = 1.0e-3*10.0**(PAO_log/10.0)#b/c AOM power is in dBm
        gamma = 2*np.pi*21.87e6
        model = lambda x, delta, alpha, A: A*2*alpha*(x/gamma**2)/(1+(2*alpha*x/gamma**2)+4*(delta/gamma)**2) #(rabi_freq**2 = alpha * power to the aom (PAO))
        guess = self.guess(counts)
        popt, copt = curve_fit(model, PAO, counts, p0=guess)
        delta_fit = popt[0]
        alpha_fit = popt[1]
        A_fit = popt[2]
        print delta_fit, alpha_fit, A_fit
                
        plt.plot(PAO_log, model(PAO,delta_fit,alpha_fit,A_fit))
        plt.plot(PAO_log, counts,'ko')
        plt.show()
        
        return alpha_fit 
        

        
