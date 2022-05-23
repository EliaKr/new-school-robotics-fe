# importing libraries
import cv2
import numpy as np
  
# reading the image data from desired directory
img = cv2.imread("img.png")
cv2.imshow('Image',img)
  
# counting the number of pixels
number_of_all_pix = np.sum(img <= 255)
number_of_black_pix = np.sum(img < 4)

print('Number of black pixels:', number_of_black_pix)
print('Number of all pixels:', number_of_all_pix)
print('Percentage of black pixels:', (number_of_black_pix / number_of_all_pix) * 100, "%")