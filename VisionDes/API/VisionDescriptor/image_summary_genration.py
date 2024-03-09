from .DataModel.ResultObject import VisionDescriptor
import json
import requests
from pydantic import BaseModel

config = None
with open('conf.json','r') as file:
    config  = json.loads(file.read())

def genrate_URL(module:str='VB'):
    return f"http://{config.get(module).get('host')}:{config.get(module).get('port')}/{config.get(module).get('version')}/add_doc"

def visiondes_gen(visiondes:VisionDescriptor):
    ret = ""
    for des in visiondes.getVisionDes():
        ret += des+"|"
    return ret[::-1]
class VisionDescriptor_out_point:
    @staticmethod
    def send(visiondes:VisionDescriptor):
        url = genrate_URL()
        print(visiondes_gen(visiondes))
        # res = requests.post(url,json={"docs":visiondes_gen(visiondes)})
