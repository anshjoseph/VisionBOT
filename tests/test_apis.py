import requests
import json

TELEMETRY = "telemetry"
START = "start"
STOP = "stop"


print("FINDING CONFIG FILE \n\n")
config = None
with open('conf.json','r') as file:
    config  = json.loads(file.read())
def genrate_URL(module:str,service:str):
    return f"http://{config.get(module).get('host')}:{config.get(module).get('port')}/{config.get(module).get('version')}/{config.get(module).get('control_panel').get(service)}"
print("LOADING MODULE ...")
module = list(config.keys())
print(f"MODULE FOUND [{','.join(module)}]")


def test_api():
    print("MAKE CONNECTION TO MODULE")
    for key in config.keys():
        res = requests.get(genrate_URL(key,TELEMETRY))
        if res.status_code == 200:
            print(f"\t Module {key} is connected")
            print(f"\t Status: {res.json().get('status')}")
            print(f"\t Message: {res.json().get('message')}")
        else:
            print(f"\t Module {key} is not connected")
        res.close()