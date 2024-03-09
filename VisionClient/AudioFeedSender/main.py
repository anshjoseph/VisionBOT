from fastapi import FastAPI, APIRouter
from audio_stream import AudioStream
import uvicorn
import json

config = None
with open('conf.json','r') as file:
    config  = json.loads(file.read())
config_CAFS = config.get('CAFS')
app = FastAPI()

class Client_VFS:
    def __init__(self) -> None:
        self.__version = config_CAFS.get('version')
        self.router = APIRouter()
        self.url = f"http://{config.get('VB').get('host')}:{config.get('VB').get('port')}/{config.get('VB').get('version')}/query"
        self.audio_strm = AudioStream(config_CAFS.get('name'),self.url,config_CAFS.get("voice_id"),config_CAFS.get('voice_rate'))
        # ROUTES
        self.router.add_api_route(f"/{self.__version}/stop",self.stop,methods=["GET"])
        self.router.add_api_route(f"/{self.__version}/telemetry",self.telemetry,methods=['GET'])
        self.router.add_api_route(f"/{self.__version}/start",self.start,methods=["GET"])
    
    async def telemetry(self):
        return self.audio_strm.telemetry()
    async def start(self):
        return self.audio_strm.start()
    async def stop(self):
        return self.audio_strm.stop()
    

client_vfs = Client_VFS()
app.include_router(client_vfs.router)
if __name__ == "__main__":
    uvicorn.run("main:app", host=config_CAFS.get('host'), reload=config_CAFS.get('reload'), port=config_CAFS.get('port'))

