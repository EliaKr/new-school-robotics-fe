# importing libraries
import cv2
import numpy as np
  
# reading the image data from desired directory
img = cv2.imread("img.png")
cv2.imshow('Image',img)
  
# counting the number of pixels in the whole image
#number_of_all_pix = np.sum(img <= 255)
#number_of_black_pix = np.sum(img < 4)

#print('Number of black pixels:', number_of_black_pix)
#print('Number of all pixels:', number_of_all_pix)
#perc = (number_of_black_pix / number_of_all_pix) * 100
#print('Percentage of black pixels:', perc, "%")

#crop region 1
#cropped = img[start_row:end_row, start_col:end_col]
left_wall = img[0:500, 0:600]

#check left cropped region
number_of_all_pix = np.sum(left_wall <= 255)
number_of_black_pix = np.sum(left_wall < 4)
percblackleft = (number_of_black_pix / number_of_all_pix) * 100
print('Percentage of black pixels at the left side:', percblackleft, "%")

#check left wall
if percblackleft >= 50:
	print("turn right")
else:
	print("forward")