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
    # Facial recognition on the stitched panorama
    gray_panorama = cv.cvtColor(panorama, cv.COLOR_BGR2GRAY)
    haar_cascade = cv.CascadeClassifier('haar_face.xml')
    faces_rect = haar_cascade.detectMultiScale(gray_panorama, scaleFactor=1.1, minNeighbors=2)

    print(f'Number of faces found in the panorama = {len(faces_rect)}')

    for i, (x, y, w, h) in enumerate(faces_rect):
        cv.rectangle(panorama, (x, y), (x + w, y + h), (0, 255, 0), thickness=2)
        cv.putText(panorama, f'{i + 1}', (x, y - 10), cv.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # Display the stitched panorama with facial recognition
    cv.imshow('Panorama with Faces', panorama)
    cv.waitKey()
    cv.destroyAllWindows()
else:
    print('Error during stitching')
