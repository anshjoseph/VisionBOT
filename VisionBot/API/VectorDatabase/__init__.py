from .ChatBot import BOT
from .chroma_db_controller import VectorDB_Controller
import os


class Processing_Data:
    def __init__(self,common_conf:dict,vb_conf:dict) -> None:
        self.__common_conf = common_conf
        self.__vb_conf = vb_conf
        self.__key = os.getenv(self.__vb_conf.get('openai'))
        self.vectordb = VectorDB_Controller(self.__common_conf.get('doc_delemeter'),self.__vb_conf.get('retrive_doc'),self.__vb_conf.get('collection_up_time'))
        self.bot = BOT(self.__key,self.vectordb)
    