import numpy as np
from ion_state_detector_1d import ion_state_detector
import pylab

#load the full image and truncate it to to test image procesing of a partial image
# image = np.load('single.npy')

image = np.load('chain.npy')
image = np.reshape(image, (496, 658))
image = image[242:255, 310:390]

x_axis = np.arange(310,390)
y_axis = np.arange(242,255)
xx,yy = np.meshgrid(x_axis, y_axis)

shaped_image = image.reshape((1,13,80))
series_of_images = np.repeat(shaped_image, 1, axis = 0)

pylab.imshow(image)
positions = pylab.ginput(0)
positions = [x+np.min(x_axis) for x,y in positions]
detector = ion_state_detector(positions)

result, params = detector.guess_parameters_and_fit(xx, yy, image)

detector.report(params)
detector.graph(x_axis, y_axis, image, params, result)


best_states, confidences = detector.state_detection(image)
excitation_probability = 1 - best_states.mean(axis = 0)
print excitation_probability, confidences

