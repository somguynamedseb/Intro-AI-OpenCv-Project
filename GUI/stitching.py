import cv2 as cv

# Initialize Imgs
img1 = cv.imread('Photos/IMG_4071.jpg')
img2 = cv.imread('Photos/IMG_4072.jpg')
img3 = cv.imread('Photos/IMG_4073.jpg')
imgList = [img1, img2, img3]


def updateImgs(imgs: list):
    for i in range(imgs.__len__() - 1):
        img = cv.imread(imgs[i])
        imgList[i] = img


def run():
    # Create a stitcher object
    stitcher = cv.Stitcher.create()

    # Stitch the images
    result, panorama = stitcher.stitch(imgList)

    # Check if stitching was successful
    if result == cv.Stitcher_OK:
        print(panorama)
        cv.imshow('Panorama', panorama)
        cv.waitKey(0)
        cv.destroyAllWindows()
    else:
        print('Error during stitching')
