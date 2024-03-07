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
while True:
    command = input(">> ")
    __command = command.split(" ")
    if command in ["help","h"]:
        print("""
              NOTE: please take care of case of alphabet

              q, quit: were ues to quit the function
              help,"h": for help
              start [service name]  : to start service
              stop  [service name]  : to start service
              show                  : to see attach module
              check [service name]  : to see telemetry data 
              """)
    if command in ["show"]:
        print(f"MODULE FOUND:\n\t[{','.join(module)}]")
    if __command[0] in ["start"]:
        if __command[1] in module:
            res = requests.get(genrate_URL(__command[1],START))
            if res.status_code == 200:
                print("SUCCEFUL: module processor start working")
            else:
                print("Newtork Error")
            res.close()
        else:
            print("error: module not found")
    if __command[0] in ["stop"]:
        if __command[1] in module:
            res = requests.get(genrate_URL(__command[1],STOP))
            if res.status_code == 200:
                print("SUCCEFUL: module processor stop working")
            else:
                print("Newtork Error")
            res.close()
        else:
            print("error: module not found")
    if __command[0] in ["check"]:
        if __command[1] in module:
            res = requests.get(genrate_URL(__command[1],TELEMETRY))
            if res.status_code == 200:
                print(f"MODULE {__command[1]}")
                print(f"\t Status: {res.json().get('status')}")
                print(f"\t Message: {res.json().get('message')}")
            else:
                print("Newtork Error")
            res.close()
        else:
            print("error: module not found")

    if command in ["q","quit"]:
        break