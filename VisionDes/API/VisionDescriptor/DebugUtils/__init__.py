import json
from typing import Self
class DebugPrinter:
   
    def __init__(self,module:str='VD') -> None:
        self.module = module
        config = None
        with open('conf.json','r') as file:
            config  = json.loads(file.read())
        self.config_VD = config.get(self.module )
        
    def print(self,text:str):
        if self.config_VD.get('debug'):
            print(text)
    
        
