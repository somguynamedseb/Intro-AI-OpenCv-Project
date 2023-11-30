import cv2 as cv

# Load images for panorama stitching
img1 = cv.imread('IMG_4071.jpg')
img2 = cv.imread('IMG_4072.jpg')
img3 = cv.imread('IMG_4073.jpg')

print(img1.shape)
print(img2.shape)
print(img3.shape)


# Create a stitcher object
stitcher = cv.Stitcher.create()

# Stitch the images
result, panorama = stitcher.stitch((img1, img2, img3))

# Check if stitching was successful
if result == cv.Stitcher_OK:
    print(panorama)
    cv.imshow('Panorama', panorama)
    cv.waitKey(0)
    cv.destroyAllWindows()
else:
    print('Error during stitching')
