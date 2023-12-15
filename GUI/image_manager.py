import os
from ultralytics import YOLO
from PIL import Image
import cv2 as cv
import PySimpleGUI as sg
import io
from io import BytesIO
import datetime


# model = YOLO('C:\Users\sebas\Documents\GitHub\Intro-AI-OpenCv-Project\GUI\last.pt')
model = YOLO('train3/weights/last.pt')

class image_manager:
    def __init__(self):
        self.img_arr = []  # array of images for stitching
        self.detected_img = None  # directory of most recent detected image
        self.face_count = -1  # detected faces
        # self.model = YOLO('train3/weights/last.pt')

    def add_image_list(self, imgDIR):
        self.img_arr = imgDIR

    def clear_images(self):
        self.img_arr = []

    def stitch_images(self) -> [str]:  ##returns DIR of stiched img
        # Read images and store them in a list
        images = [cv.imread(img) for img in self.img_arr]
        # Create a stitcher object
        stitcher = cv.Stitcher.create()
        # Perform the stitching process
        status, stitched_img = stitcher.stitch(images)
        if status == cv.Stitcher_OK:
            # Convert the stitched image to a PIL Image
            stitched_pil_image = Image.fromarray(cv.cvtColor(stitched_img, cv.COLOR_BGR2RGB))
            # Define the size to which you want to scale the image
            max_width, max_height = 800, 600  # Adjust these values as needed
            # Calculate the scaling factor, maintaining the aspect ratio
            scaling_factor = min(max_width / stitched_pil_image.width, max_height / stitched_pil_image.height)
            # Compute the new size
            new_size = (int(stitched_pil_image.width * scaling_factor),
                        int(stitched_pil_image.height * scaling_factor))
            # Resize the image
            stitched_pil_image = stitched_pil_image.resize(new_size, Image.Resampling.LANCZOS)
            bio = io.BytesIO()
            stitched_pil_image.save(bio, format="PNG")
            bio.seek(0)
            imgBytes = bio.read()

            # timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            # filename = f"last_stitched_Image_{timestamp}"
            # image = Image.open(BytesIO(imgBytes))
            # image.save(os.path.join(os.path.dirname(__file__), filename))

            return imgBytes
        else:
            sg.popup_error('Image stitching failed!', 'Error code: ' + str(status))
            return None

    def detect_faces(self, imgDIR) -> [str, int]:  # returns DIR of output img
        if isinstance(imgDIR, bytes):
            img = Image.open(BytesIO(imgDIR))
        else:
            img = Image.open(imgDIR)
        results = model.predict(source=img, save=True)  # save plotted images
        d = results[0].save_dir
        DIR = os.path.join(d, (os.listdir(d)[0]))  # error is that there is no image actually saved in the predict file
        self.detected_img = DIR
        self.face_count = len(results[0].boxes.xyxy)
        self.detected_img = self.detected_img.replace("\\", "/")
        return [self.detected_img, self.face_count]

    def get_face_count(self) -> int:
        return self.face_count
