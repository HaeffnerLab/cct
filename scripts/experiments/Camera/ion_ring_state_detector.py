import numpy as np
import lmfit
import math
import cv2
import datetime

class ion_ring_state_detector(object):
    
    def __init__(self):
        pass
                    
    def state_detection(self, image):
        '''
        given the image and the parameters of the reference images with all ions bright, determines
        which ions are currently darks
        '''
        if self.fitted_gaussians is None:
            raise Exception("Fitted parameters not provided")
        if image.ndim == 2:
            #if only a single image is provided, shape it to be a 1-long sequence
            image = image.reshape((1, image.shape[0],image.shape[1]))
        state, confidence = self.fitting_error_state(self.all_state_combinations, image)
        return state, confidence
    
    def graph(self, x_axis, y_axis, image, params, result = None):
        #plot the sample data
        from matplotlib import pyplot
        pyplot.contourf(x_axis, y_axis, image, alpha = 0.5)
        #plot the fit
        #sample the fit with more precision
        x_axis_fit = np.linspace(x_axis.min(), x_axis.max(), x_axis.size * 5)
        y_axis_fit = np.linspace(y_axis.min(), y_axis.max(), y_axis.size * 5)
        xx, yy = np.meshgrid(x_axis_fit, y_axis_fit)
        fit = self.ion_model(params, xx, yy)
        pyplot.contour(x_axis_fit, y_axis_fit, fit, colors = 'k', alpha = 0.75)
        if result is not None:
            pyplot.annotate('chi sqr {}'.format(result.redchi), (0.5,0.8), xycoords = 'axes fraction')
        pyplot.tight_layout()
        pyplot.show()
        
    def find_radial_positions(self, image, ring_center,threshold):     
        #img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 

        img_gray = np.array(image, dtype = np.uint8)
        template = cv2.imread('/home/space-time/Desktop/ion_reference.bmp',0)
        w,h = template.shape[::-1]
        
        res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
        loc = np.where( res >= threshold)
        blur = cv2.GaussianBlur(img_gray,(5,5),0)
        
        ion_locations = []
        for pt in zip(*loc[::-1]):
            max_loc = cv2.minMaxLoc(blur[pt[1]:pt[1]+h,pt[0]:pt[0]+w])
            max_pixel = np.sum(zip(max_loc[3],pt),1)
            single_ion_loc = (max_pixel[0],max_pixel[1])
            cv2.circle(img_gray, single_ion_loc, 3, (0,0,255), 1)
            if single_ion_loc not in ion_locations:
                ion_locations.append(single_ion_loc)
        
        filename = datetime.datetime.strftime(datetime.datetime.now(), '%H_%M_%S_%f.png')
        cv2.imwrite('/home/space-time/Desktop/'+filename,img_gray)
        
        radial_locations = []
        for loc in ion_locations:
            r_pos = ((ring_center[0]-loc[0])**2. + (ring_center[1]-loc[1])**2.)**(1./2.)
            theta_pos = math.atan2((ring_center[1]-loc[1]),(ring_center[0]-loc[0]))
            if theta_pos < 0:
                theta_pos = theta_pos + 2*math.pi
            radial_locations.append((r_pos,theta_pos))
        
        radial_locations = sorted(radial_locations, key=lambda tup: tup[1])
        return radial_locations
    
    def compare_configs(self, initial_config, final_config,tolerance):
        initial_bright_ions = len(initial_config)
        final_bright_ions = len(final_config)
        if initial_bright_ions == 0:
            print "Warning! No ions bright"
            return None
        if initial_bright_ions != final_bright_ions:
            print "first and final images did not match ion number"
            return None
        else:
            for i in range(0,initial_bright_ions):
                position_i = initial_config[i]
                position_f = final_config[i]
                pixels_away = math.sqrt((position_i[0]-position_f[0])**2+(position_i[1]-position_f[1])**2.)
                if pixels_away > tolerance:
                    return True
            return False
                
