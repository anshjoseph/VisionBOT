import chromadb
from uuid import uuid4
import datetime
import time
from threading import Thread, Event
import string
import random

class vectorDB:
    def __init__(self,delemeter:str,doc_ret:int) -> None:
        self.controller_id:str = str(uuid4)
        
        self.last_modify = datetime.datetime.now()
        
        self.delete()

        self.__delemeter = delemeter
        self.__doc_ret = doc_ret
        
    def add_documents(self,doc:str):
        self.delete()
        _docs = doc.split(self.__delemeter)
        print(_docs)
        self.__collection.add(documents=_docs,metadatas=[{"source": doc[:5]} for doc in _docs],ids=[str(uuid4())[:10] for _ in range(len(_docs))])
    def query(self,query:str):
        results = self.__collection.query(
            query_texts=[query],
            n_results=self.__doc_ret
        )
        return results
    def delete(self):
        self.__client = chromadb.Client()
        self.__collection_id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        self.__collection = self.__client.create_collection(self.__collection_id)
        print(self.__collection_id) 
    







class VectorDB_Controller:
    def __init__(self,delemeter:str,doc_ret:int,update_time:int) -> None:
        self.__memory_buffer_vector_space:vectorDB = vectorDB(delemeter,doc_ret)
        self.update_time = update_time
        self.__docs:list = []
        self.__stop = Event()
        self.is_runing = False
        self.__processor:Thread = None

    def add_docs(self,docs:str):
        self.__docs.append(docs)

    def __runner(self):
        # threading input
        print("hello")

        while not self.__stop.is_set():
            if len(self.__docs) > 0:
                self.__memory_buffer_vector_space.delete()
                self.__memory_buffer_vector_space.add_documents(self.__docs.pop(0)) 
            print(f"sleep {self.update_time}")
            time.sleep(self.update_time)
            
    def query(self,question:str):
        return self.__memory_buffer_vector_space.query(question)
    
    def start(self):
        self.is_runing = True
        self.__processor = Thread(target=self.__runner)
        self.__processor.start()

    def stop(self):
        self.__stop.set()
        self.__processor = None
        self.is_runing = False

    def telemetry(self)->dict:
        status = "Stop"
        if self.is_runing:
            status = "Run"
        return {"status":status,'message':f"last vector buffer space updated {self.__memory_buffer_vector_space.last_modify}" }