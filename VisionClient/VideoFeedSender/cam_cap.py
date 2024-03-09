import cv2 
from uuid import uuid4
from threading import Thread, Event
import time
import requests
import os

class CameraCapture:
    def __init__(self,cap_delay:int,temp_loc:str,cam_id:int,upload_endpoint:str) -> None:
        print(cam_id)
        self.vid = cv2.VideoCapture(cam_id)
        self.cam_id = cam_id 
        self.cap_delay = cap_delay
        self.temp_loc = temp_loc
        self.is_running = False
        self.upload_endpoint = upload_endpoint
        self.__stop = Event()
        self.__processor = None
        self.frames:list = []
    def __runner(self):
        while not self.__stop.is_set():
            ret, frame = self.vid.read()
            if ret:
                path = f"{self.temp_loc}/{uuid4()}.jpg"
                self.frames.append(path) 
                cv2.imwrite(path, frame)
                files = {'file': (path.split("/")[-1],open(path, 'rb'),'image/jpeg')}
                res = requests.post(self.upload_endpoint,files=files)
                print(res.content)
                os.remove(path)
            time.sleep(self.cap_delay)
    def start(self):
        self.is_running = True
        self.__processor = Thread(target=self.__runner)
        self.__stop = Event()
        self.__processor.start()
        return "DONE"
    def stop(self):
        self.is_running = False
        self.__stop.set()
        return "DONE"
    def telemetry(self):
        status = "Stop"
        if self.is_running:
            status = "Run"
        return {"status":status,'message':f"camera is mounted id: {self.cam_id} and process status {status} with delay of {self.cap_delay}, temp location {self.temp_loc} accumalate {len(self.frames)} frames" }