from ultralytics import YOLO
from uuid import uuid4
import numpy as np
from typing import List
from .DataModel.ResultObject import VisionDescriptor
class ObjectDectionResult:
    def __init__(self) -> None:
        self.__result_data:dict = {} ## key is unique id : {class name, confidence percentage,crop image} 
    def add_element(self,class_name:str,confidence:float,obj_img:np.array):
        temp_obj_id = str(uuid4())
        self.__result_data[temp_obj_id] = {
            "class_name":class_name,
            "confidence":confidence,
            "obj_img":obj_img
        }
        return temp_obj_id
    def getByClassName(self,class_name:str)->List[dict]:
        "you can get by class or by id"
        out:List[dict] = []
        for key in self.__result_data.keys():
            temp_obj = self.__result_data.get(key)
            if temp_obj.get('class_name') == class_name:
                out.append(temp_obj)
        return out
    def getByID(self,id:str) -> dict:
        return self.__result_data.get(id)
    def getAll(self) -> dict:
        return self.__result_data
    def __repr__(self) -> str:
        out = ""
        for ids in self.__result_data.keys():
            out += f"Objects id: {ids}\n"
            for ele in self.__result_data.get(ids):
                out += f"\t{ele} : {self.__result_data.get(ids).get(ele)}\n"
        return out
class ImageObjectDection:
    def __init__(self,conf_object:dict,debug) -> None:
        self.__model = YOLO(conf_object.get("model_object_dectection"))
        self.__debug = debug
    def startProcessing(self,mat:np.array,visiondes:VisionDescriptor) -> ObjectDectionResult:
        results = self.__model(mat,save=True,conf=0.5)
        output = ObjectDectionResult()
        for result in results:
            names = result.names
            classes = result.boxes.cls
            temp_dict = dict()
            for index,class_idx in enumerate(classes.detach().numpy()):
                ## ERROR
                x,y,w,h = np.array(result.boxes.xyxy[index].detach().numpy(),dtype=np.int32)
                crop_img:np.array = mat[y:h,x:w]
                # print(names)
                object_id = output.add_element(names[class_idx],result.boxes.conf[index].detach().numpy(),crop_img)
                visiondes.add_element(object_id)
                visiondes.add_element_attribute(object_id,"type",names[class_idx])
                if temp_dict.get(names[class_idx]) == None:
                    temp_dict[names[class_idx]] = 0
                temp_dict[names[class_idx]] += 1
                visiondes.add_element_attribute(object_id,"confidence",result.boxes.conf[index].detach().numpy())
            if len(temp_dict) > 0:
                visiondes.add_element_attribute("main_scene","summary",f"there are {' '.join([str(temp_dict[key])+' '+str(key) for key in temp_dict ])}")
            else:
                visiondes.add_element_attribute("main_scene","summary",f"we didn't any objects")
        return output
