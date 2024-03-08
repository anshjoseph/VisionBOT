from fastapi import FastAPI, APIRouter
import uvicorn
from VectorDatabase import Processing_Data
from VectorDatabase.DataModel.doc import Doc
import json

config = None
with open('conf.json','r') as file:
    config  = json.loads(file.read())
config_VB = config.get('VB')
app = FastAPI()

class VisionBOT:
    def __init__(self) -> None:
        self.__version = config_VB.get('version')
        self.router = APIRouter()
        self.data_processor = Processing_Data(config.get('Common_Conf'),config_VB)
        # ROUTES
        self.router.add_api_route(f"/{self.__version}/add_doc", self.add_doc, methods=["POST"])
        self.router.add_api_route(f"/{self.__version}/query", self.query, methods=["GET"])
        self.router.add_api_route(f"/{self.__version}/stop",self.stop,methods=["GET"])
        self.router.add_api_route(f"/{self.__version}/telemetry",self.telemetry,methods=['GET'])
        self.router.add_api_route(f"/{self.__version}/start",self.start,methods=["GET"])
    async def add_doc(self,doc:Doc):
        self.data_processor.vectordb.add_docs(doc.docs)
        return "DONE"
    async def query(self,question:str):
        return self.data_processor.bot.query(question)
    async def telemetry(self):
        return self.data_processor.vectordb.telemetry()
    async def start(self):
        self.data_processor.vectordb.start()
        return "DONE"
    async def stop(self):
        self.data_processor.vectordb.stop()
        return "DONE"
    
vision_bot = VisionBOT()
app.include_router(vision_bot.router)

if __name__ == "__main__":
    print(config_VB.get('port'))
    uvicorn.run("main:app", host=config_VB.get('host'), reload=config_VB.get('reload'), port=config_VB.get('port'))
