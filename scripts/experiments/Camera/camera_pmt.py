import numpy as np

def detect_pmt(params, xx, yy, images):
    results = []
    confs = []
    if images.ndim == 2:
        #if only a single image is provided, shape it to be a 1-long sequence
        images = images.reshape((1, images.shape[0],images.shape[1]))

    for i in xrange(images.shape[0]):
        res, conf = detect_pmt_single(params, xx, yy, images[i,:,:])
        results.append(res)
        confs.append(conf)
    return np.array(results), np.array(confs)

def detect_pmt_single(params, xx, yy, image):
    xmin = xx.min()
    ymin = yy.min()
    x0 = params['center_x'].value
    y0 = params['center_y'].value 
    dx = int(round(params['spacing'].value / 2.0 * 1.27 )) 
    w =  params['sigma'].value * 1.4
    back = params['background_level'].value
    x_index = int(round(x0 - xmin))
    y_index = int(round(y0 - ymin))
    i1 = [x_index+dx, y_index]
    s1 = np.sum(image[i1[1]-w:i1[1]+w,i1[0]-w:i1[0]+w]) / (4*w**2)
    i2 = [x_index-dx, y_index]
    s2 = np.sum(image[i2[1]-w:i2[1]+w,i2[0]-w:i2[0]+w]) / (4*w**2)
    if s1 > back:
        v1 = 1
    else:
        v1 = 0

    if s2 > back:
        v2 = 1
    else:
        v2 = 0
#    print v1,v2,s1, s2, back, i1, i2, x0+dx, x0-dx
#    import IPython
#    IPython.embed()
    return [v1,v2], [s1]
    
