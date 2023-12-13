import os
from ultralytics import YOLO
from PIL import Image
import cv2 as cv

model = YOLO("runs/detect/train4/weights/last.pt")

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

    def stich_images(self)->[str,int]: ##returns DIR of stiched img
        raise NotImplementedError

    #detects faces within stored images
    def detect_faces(self)->str: ##returns DIR of output img
        if self.img_arr == []:
            raise ValueError("No images to detect faces in")
        if self.img_arr != []:
            # if self.saved_img ==None:
                # self.saved_img = self.stich_images()
            img = Image.open(self.saved_img)
            results = model.predict(source=img, save=True)  # save plotted images
            DIR = os.path.join(results[0].save_dir,(os.listdir(results[0].save_dir))[0])
            self.detected_img = DIR
            self.face_count = len(len(results[0].boxes.xyxy))
        return [self.detected_img,self.face_count]

    def face_count(self)->int:
        return self.face_count

