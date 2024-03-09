from .DebugUtils import DebugPrinter
from .image_object_dectection import ImageObjectDection
import numpy as np
from threading import Thread, Event
import time
from uuid import uuid4
from .image_text_processing import TestExtraction
from .DataModel.ResultObject import VisionDescriptor
from .image_summary_genration import VisionDescriptor_out_point

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Processing_Data:
    def __init__(self,config_VD:dict,debug:DebugPrinter) -> None:
        self.config_VD = config_VD
        __metaclass__ = Singleton
        self.debug = debug
        self.id = str(uuid4)
        # features
        self.__image_object_dection = ImageObjectDection(self.config_VD,self.debug)
        # Thread
        self.__processing_thread:Thread = None
        # JOB POOL
        self.queue_full:bool = False
        self.stop = Event()
        self.__pipeline_queue:list  = []
        self.__pipeline_queue_staging_area = []
        # CONF
        self.__job_sleep = config_VD.get('job_sleep')
        self.__job_queue_size = config_VD.get('job_queue_size')
        self.__job_statging_area= config_VD.get('job_statging_area')
        ## Toggle Switch
        self.__fea_object_dection = config_VD.get('features').get('Object_dection')
        self.__fea_OCR_enable = config_VD.get('features').get('OCR_enable')
        self.__fea_Color_intensity_dection = config_VD.get('features').get('Color_intensity_dection')
        

        # FLAG
        self.__process_flag = False
    
    def stop_process(self):
        self.stop.set()
        self.__process_flag = False
        # self.__processing_thread.raise_exception(SystemExit)
        # self.__processing_thread.join()
    def add_to_piepeline_queue(self,mat:np.array):
        if len(self.__pipeline_queue_staging_area) < self.__job_statging_area or len(self.__add_to_piepeline_queue) < self.__job_queue_size:
            self.queue_full = False
        else:
            self.queue_full = True
        if len(self.__pipeline_queue) < self.__job_queue_size:
            if len(self.__pipeline_queue_staging_area) == 0:
                self.__pipeline_queue.append(mat)
            else:    
                while len(self.__pipeline_queue) < self.__job_queue_size:
                    self.__pipeline_queue.append(self.__pipeline_queue_staging_area.pop(0))
                
                if len(self.__pipeline_queue) < self.__job_queue_size:
                    self.__pipeline_queue.append(mat)
                else:
                    self.__pipeline_queue_staging_area.append(mat)
               
        else:
            if len(self.__pipeline_queue_staging_area) < self.__job_statging_area:
                self.__pipeline_queue_staging_area.append(mat)
            else:
                self.queue_full = True



    def __run_job(self):
        "MAIN PIPE LINE FUNCTION"
        while not self.stop.is_set():
            self.debug.print(f"Object id: {self.id}")
            self.debug.print("thread is start processing")
            if len(self.__pipeline_queue) > 0:
                self.debug.print("new job is stating")
                vision_descriptor = VisionDescriptor()
                vision_descriptor.add_element("main_scene")
                mat:np.array = self.__pipeline_queue.pop(0)
                results = None
                ## main feature pipe
                if self.__fea_object_dection:
                    results = self.__image_object_dection.startProcessing(mat,vision_descriptor)
                if self.__fea_OCR_enable:
                    if len(results.getAll()) > 0:
                        TestExtraction.run(results,vision_descriptor)
                    TestExtraction.read_image(mat,vision_descriptor)
                
                # print(next(vision_descriptor.getVisionDes()))
                VisionDescriptor_out_point.send(vision_descriptor)
                
            
            
            self.debug.print(f"thread is sleeping to {self.__job_sleep} sec")
            time.sleep(self.__job_sleep)
    
    
    def get_telemetry_data(self):
        print(not self.stop.is_set())
        
        status = 'Normal'
        if len(self.__pipeline_queue_staging_area) > len(self.__pipeline_queue_staging_area)//2:
            status = 'Stress'
        if len(self.__pipeline_queue) == 0 and self.__process_flag:
            status = "Idel"
        if len(self.__pipeline_queue) > len(self.__pipeline_queue)//4:
            status = "Modrate"
        if not self.__process_flag:
            status = 'Stop'    
        return {"no_jobs":len(self.__pipeline_queue),"no_jobs_at_statging":len(self.__pipeline_queue_staging_area),"message":f"job_quey has {len(self.__pipeline_queue)} remaining space {self.__job_queue_size} jobs and job stagaing are has {len(self.__pipeline_queue_staging_area)} out of {self.__job_statging_area}","status":status}
    def run_pipeline(self):
        self.__processing_thread = Thread(target=self.__run_job)
        self.__processing_thread.start()
        self.__process_flag = True
