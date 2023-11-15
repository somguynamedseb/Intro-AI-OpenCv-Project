# Import necessary libraries
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

    # Load the Haar Cascade classifier for face detection
    haar_cascade = cv.CascadeClassifier('haar_face.xml')

    # Detect faces in the panorama using the Haar Cascade
    faces_rect = haar_cascade.detectMultiScale(panorama, scaleFactor=1.1, minNeighbors=2)

    # Print the number of faces found in the panorama
    print(f'Number of faces found in the panorama = {len(faces_rect)}')

    # Calculate the average size of detected faces
    face_sizes = np.array([w * h for _, _, w, h in faces_rect])
    avg_face_size = np.mean(face_sizes)

    # Define a threshold for filtering outliers
    threshold = 1  # You can adjust this threshold based on your needs

    # Filter out faces that deviate significantly from the average size
    filtered_faces_rect = [rect for rect in faces_rect if abs(rect[2] * rect[3] - avg_face_size) < threshold * avg_face_size]

    # Print the number of faces after filtering
    print(f'Number of filtered faces = {len(filtered_faces_rect)}')

    # Draw rectangles around the filtered faces and annotate with numbers
    for i, (x, y, w, h) in enumerate(filtered_faces_rect):
        cv.rectangle(panorama, (x, y), (x + w, y + h), (0, 255, 0), thickness=2)
        cv.putText(panorama, f'{i + 1}', (x, y - 10), cv.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # Display the stitched panorama with facial recognition
    cv.imshow('Panorama with Faces', panorama)
    cv.waitKey()
    cv.destroyAllWindows()
else:
    # Print an error message if stitching was not successful
    print('Error during stitching')
