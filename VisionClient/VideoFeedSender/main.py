from fastapi import FastAPI, APIRouter, BackgroundTasks, UploadFile
from cam_cap import CameraCapture
import uvicorn
import json

config = None
with open('conf.json','r') as file:
    config  = json.loads(file.read())
config_CVFS = config.get('CVFS')
app = FastAPI()

class Client_VFS:
    def __init__(self) -> None:
        self.__version = config_CVFS.get('version')
        self.router = APIRouter()
        self.url = f"http://{config.get('VD').get('host')}:{config.get('VD').get('port')}/{config.get('VD').get('version')}/push_imag"
        self.cam_cap = CameraCapture(config_CVFS.get('cam_sleep'),config_CVFS.get('temp'),config_CVFS.get("cam_id"),self.url)
        # ROUTES
        self.router.add_api_route(f"/{self.__version}/stop",self.stop,methods=["GET"])
        self.router.add_api_route(f"/{self.__version}/telemetry",self.telemetry,methods=['GET'])
        self.router.add_api_route(f"/{self.__version}/start",self.start,methods=["GET"])
    
    async def telemetry(self):
        return self.cam_cap.telemetry()
    async def start(self):
        return self.cam_cap.start()
    async def stop(self):
        return self.cam_cap.stop()
    

client_vfs = Client_VFS()
app.include_router(client_vfs.router)
if __name__ == "__main__":
    uvicorn.run("main:app", host=config_CVFS.get('host'), reload=config_CVFS.get('reload'), port=config_CVFS.get('port'))

