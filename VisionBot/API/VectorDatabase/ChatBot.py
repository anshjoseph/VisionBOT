import openai
from .chroma_db_controller import VectorDB_Controller
class BOT:
    def __init__(self,key:str,vectorDB_controller:VectorDB_Controller) -> None:
        openai.api_key = key
        self.vectorDB_controller:VectorDB_Controller = vectorDB_controller
    def query(self,query:str)->str:
        messages = [{"role": "system", "content": "You are a assistant help to blind people to understand the world."}]
        if self.vectorDB_controller.is_runing:
            arc_data = self.vectorDB_controller.query(query)
            print(arc_data)
            # change 
            messages.append({"role": "user", "content": f"{arc_data} \nanswer the question from above world describtion"})
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
            return {'answer':response['choices'][0]['message']['content'],"succes":True,"message":"service properly"}
        return {"answer":None,"succes":False,"message":"it seems the the VB module is not running use control panel"}