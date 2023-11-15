import cv2 as cv
import numpy as np

# Load images for panorama stitching
img1 = cv.imread('IMG_4071.jpg')
img2 = cv.imread('IMG_4072.jpg')
img3 = cv.imread('IMG_4073.jpg')

# Create a stitcher object
stitcher = cv.Stitcher_create()

# Stitch the images
result, panorama = stitcher.stitch((img1, img2, img3))

# Check if stitching was successful
if result == cv.Stitcher_OK:
    cv.imshow('Panorama', panorama)
    cv.waitKey()
    cv.destroyAllWindows()
else:
    print('Error during stitching')