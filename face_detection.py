#pylint:disable=no-member
#  https://youtu.be/oXlwWbU8l2o?si=36WAVGgEBl8pugIO&t=67
# go here ^^ for the packages that we need for the file to work
# havent tested in pycharm yet, remove when tested and working
import cv2 as cv

img = cv.imread(r'Students_in_Large_Classroom_with_Laptops.jpg')
# cv.imshow('Group of 5 people', img)

gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
# cv.imshow('Gray People', gray)

haar_cascade = cv.CascadeClassifier('haar_face.xml')

faces_rect = haar_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=2)

print(f'Number of faces found = {len(faces_rect)}')

for (x,y,w,h) in faces_rect:
    cv.rectangle(img, (x,y), (x+w,y+h), (0,255,0), thickness=2)
cv.imshow('Detected Faces', img)
# img2 = cv.resize(img, (500,500))
# img3 = cv.resize(img, (1000,1000))


cv.waitKey(0)