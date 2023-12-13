import os
from ultralytics import YOLO
from PIL import Image
import cv2 as cv

class image_manager:
    def __init__(self):
        self.img_arr = []  ## array of images for stitching
        self.saved_img = None ## directory of stitched or non stiched image
        self.detected_img = None ##directory of most recent detected image
        self.face_count = -1 ## detected faces


    def add_image(self,imgDIR):
        self.img_arr = [self.img_arr, imgDIR]

    def clear_images(self):
        self.img_arr = []

    def stich_images(self):
        raise NotImplementedError

    #detects faces within stored images
    def detect_faces(self)->str: ##returns DIR of output img
        raise NotImplementedError

    def face_count(self)->int:
        return self.face_count

