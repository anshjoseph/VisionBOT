from fastapi import FastAPI, APIRouter, BackgroundTasks, UploadFile
import numpy as np
import uvicorn
import json
import cv2
from VisionDescriptor import DebugPrinter, ImageObjectDection, Processing_Data
import os

config = None
with open('conf.json','r') as file:
    config  = json.loads(file.read())
config_VD = config.get('VD')
app = FastAPI()
debug = DebugPrinter()
__processor = Processing_Data(config_VD,debug)


class VisionAPI:
    def __init__(self,debug,__processor) -> None:
        debug.print("VisionAPI object created")
        self.__version = config_VD.get('version')
        self.router = APIRouter()
        self.debug:DebugPrinter = debug
        self.__processor:Processing_Data = __processor
        
        # ROUTES
        self.router.add_api_route(f"/{self.__version}/push_imag", self.push_imag, methods=["POST"]) # can mod
        self.router.add_api_route(f"/{self.__version}/stop",self.stop_processing_pipeline,methods=["GET"])
        self.router.add_api_route(f"/{self.__version}/telemetry",self.__processor.get_telemetry_data,methods=['GET'])
        self.router.add_api_route(f"/{self.__version}/start",self.start_processing_pipeline,methods=["GET"])
    
    # THREAD PROCESS 
    def start_processor(self):
        self.__processor.run_pipeline()
    def stop_processor(self):
        self.__processor.stop_process()

    # UTIL FUNCTION
    async def __bytes_to_mat(self,file:UploadFile):
        bytes_array = np.asarray(bytearray(await file.read()), dtype="uint8") 
        return cv2.imdecode(bytes_array, cv2.IMREAD_COLOR)
    
    # ROUTES
    async def start_processing_pipeline(self):
        vision_api.start_processor()
        return "Done"
    async def stop_processing_pipeline(self):
        self.stop_processor()
        return "Done"
    async def push_imag(self,file:UploadFile,):
        if(file.content_type in ['image/jpeg','image/png']):
            self.debug.print(f"file name: {file.filename}")
            image:np.array = await self.__bytes_to_mat(file)
            self.__processor.add_to_piepeline_queue(image)
            if self.__processor.queue_full:
                return {"get_file":True,"message":"file was recieve correctly but can't add job,queue is full","job_add":False}
            else:
                return {"get_file":True,"message":"file was accepted succesfully and processing is started","job_add":True}
        return {"get_file":False,"message":"worng type of file were send only jpeg and png were support by the server","job_add":False}

vision_api = VisionAPI(debug,__processor)
app.include_router(vision_api.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host=config_VD.get('host'), reload=config_VD.get('reload'), port=config_VD.get('port'))