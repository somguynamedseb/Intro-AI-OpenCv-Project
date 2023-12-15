import os
from ultralytics import YOLO
from PIL import Image
import cv2 as cv
import PySimpleGUI as sg
import io
from io import BytesIO
import datetime
import image_manager


imgM = image_manager.image_manager()
temp = imgM.detect_faces("Students_in_Large_Classroom_with_Laptops.jpg")
print(temp)



