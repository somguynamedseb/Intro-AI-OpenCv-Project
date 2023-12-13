import os
from ultralytics import YOLO
from PIL import Image
import cv2 as cv
import io
import PySimpleGUI as sg

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

    def stich_images(self,window)->[str]: ##returns DIR of stiched img
       # Read images and store them in a list
        images = self.img_arr
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
            # Save the resized image to a BytesIO object
            bio = io.BytesIO()
            stitched_pil_image.save(bio, format="PNG")
            bio.seek(0)
            # Update the GUI to display the resized stitched image
            img = bio.read()
            window["-IMAGE-"].update(data=img)
            window[f'-IMGTEXT-'].update("Stitched Image:")
            window[f'-TOUT-'].update("")
            window["-SKIP-"].update(visible=False)
            window[f'-NEXT-'].update(visible=True)
            return img
        else:
            sg.popup_error('Image stitching failed!', 'Error code: ' + str(status))
            return None

    #detects faces within stored images
    def detect_faces(self)->[str,int]: ##returns DIR of output img
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

