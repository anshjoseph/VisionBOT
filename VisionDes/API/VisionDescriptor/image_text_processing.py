from PIL import Image
import cv2
import numpy as np
import pytesseract
from .DataModel.ResultObject import VisionDescriptor
class TestExtraction:
    @staticmethod
    def run(results,visionDes:VisionDescriptor):
        results:dict = results.getAll()
        print(results)
        for key in results.keys():
            image = Image.fromarray(cv2.cvtColor(results.get(key).get("obj_img"),cv2.COLOR_BGR2RGB))
            written:str = pytesseract.image_to_string(image)
            visionDes.add_element_attribute(key,"written",written)
    @staticmethod
    def read_image(mat:np.array,visionDes:VisionDescriptor):
        image = Image.fromarray(cv2.cvtColor(mat,cv2.COLOR_BGR2RGB))
        written:str = pytesseract.image_to_string(image)
        visionDes.add_element_attribute('main_scene','written',written)
    
        

