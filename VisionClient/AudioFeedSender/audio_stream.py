import speech_recognition
import pyttsx3
from threading import Thread, Event
import requests
from urllib.parse import quote 

class AudioStream:
    def __init__(self,name:str,upload_endpoint:str,voice_id:int,voice_rate:int) -> None:
        self.UserVoiceRecognizer = speech_recognition.Recognizer()
        self.name = name
        self.voice_id = voice_id
        self.voice_rate = voice_rate
        self.gender = "MALE"
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', voice_rate)
        voices = self.engine.getProperty('voices') 
        if voice_id == 0:
            self.engine.setProperty('voice', voices[0].id)#MALE
        else:
            self.gender = "FEMALE"
            self.engine.setProperty('voice', voices[1].id)#Female
        self.is_running = False
        self.upload_endpoint = upload_endpoint
        self.__stop = Event()
        self.__processor = None
    def __speek(self,text:str):
        self.engine.say(text)
        self.engine.runAndWait()

    def __runner(self):
        while not self.__stop.is_set():
            with speech_recognition.Microphone() as UserVoiceInputSource:
                self.UserVoiceRecognizer.adjust_for_ambient_noise(UserVoiceInputSource, duration=0.5)
                UserVoiceInput = self.UserVoiceRecognizer.listen(UserVoiceInputSource)
                UserVoiceInput_converted_to_Text = self.UserVoiceRecognizer.recognize_google(UserVoiceInput)
                UserVoiceInput_converted_to_Text = UserVoiceInput_converted_to_Text.lower()

                if self.name in UserVoiceInput_converted_to_Text.split(' '):
                    res = requests.get(self.upload_endpoint+"?question=" +quote(UserVoiceInput_converted_to_Text, safe=''))
                    self.__speek(res.json().get('answer'))
    def start(self):
        self.is_running = True
        self.__processor = Thread(target=self.__runner)
        self.__stop = Event()
        self.__processor.start()
        return "DONE"
    def stop(self):
        self.is_running = False
        self.__stop.set()
        return "DONE"
    def telemetry(self):
        status = "Stop"
        if self.is_running:
            status = "Run"
        return {"status":status,'message':f"MODULE is running with parameter voice rate {self.voice_rate} and voice gender {self.gender}" }