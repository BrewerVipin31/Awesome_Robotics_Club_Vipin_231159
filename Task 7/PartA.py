import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
 
img = cv.imread('image2.png')

denoised_img = cv.fastNlMeansDenoisingColored(img, None, 17, 30, 3, 21)

# Convert the image to HSV color space
hsv_image = cv.cvtColor(denoised_img, cv.COLOR_BGR2HSV)

# Define the lower and upper bounds for the blue color
lower_blue = np.array([90, 50, 50])
upper_blue = np.array([130, 255, 255])

# Create a mask for the blue color
mask = cv.inRange(hsv_image, lower_blue, upper_blue)

# Apply the mask to the original image
masked_image = cv.bitwise_and(denoised_img, denoised_img, mask=mask)

# Denoise the masked image
denoised_image = cv.fastNlMeansDenoisingColored(masked_image, None, 10, 10, 7, 21)

# Convert the denoised image to HSV color space
denoised_hsv = cv.cvtColor(denoised_image, cv.COLOR_BGR2HSV)

# Define the lower and upper bounds for the blue color
lower_blue = np.array([90, 50, 50])
upper_blue = np.array([130, 255, 255])

# Create a mask for the non-blue areas in the denoised image
mask = cv.inRange(denoised_hsv, lower_blue, upper_blue)
mask = cv.bitwise_not(mask)

# Apply the mask to the original image
background = cv.bitwise_and(denoised_img, denoised_img, mask=mask)

# Inverse the mask
mask = cv.bitwise_not(mask)

# Apply the mask to the denoised image
foreground = cv.bitwise_and(denoised_image, denoised_image, mask=mask)

# Combine the foreground and background to get the final image
result = cv.add(background, foreground)

b,g,r = cv.split(result)       # get b,g,r
result = cv.merge([r,g,b])     # switch it to rgb
b,g,r = cv.split(img)       # get b,g,r
img = cv.merge([r,g,b])     # switch it to rgb

#Displaying the images
plt.subplot(121),plt.imshow(img)
plt.subplot(122),plt.imshow(result)
plt.show()