 import cv
orig = cv.LoadImage("rot.png")
cv.Flip(orig, flipMode=-1)
cv.ShowImage('180_rotation', orig)
cv.WaitKey(0)
