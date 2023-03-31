from settings import *
import pygame
import io
import pyaudio
import boto3
import wave
import time
import base64
import gzip

class Audio:
    def __init__(self, game_status):
        #self.client = boto3.client('lexv2-runtime')
        self.chunk = 1024
        self.sample_format = pyaudio.paInt16
        self.channels = 1
        self.rate = 16000
        self.seconds = 5
        
        self.game_status = game_status

    def setSessionId(self, sessionId = None):
        self.sessionId = sessionId if sessionId else self.createSessionId()

    def createSessionId(self):
        return str(time.time_ns())
    
    def setup(self,botId=None,botAliasId=None,localeId=None,sessionId=None):
        self.botId = botId if botId else BOTID
        self.botAliasId = botAliasId if botAliasId else BOTALIASID
        self.localeId = localeId if localeId else LOCALID
        self.setSessionId(sessionId)
        self.game_status.add("audio")
        self.game_status.add("action")

    def unzip(self, data):
        return gzip.decompress(base64.b64decode(data))

    def recording(self):
        audio = pyaudio.PyAudio()
        
        print("開始錄音...")
        stream = audio.open(format=self.sample_format, channels=self.channels, rate=self.rate, frames_per_buffer=self.chunk, input=True)
        frames = []

        for i in range(0, int(self.rate / self.chunk * self.seconds)):
            data = stream.read(self.chunk)
            frames.append(data)

        stream.stop_stream()
        stream.close()
        audio.terminate()

        print('錄音結束...')

        wf = wave.open("input.wav", 'wb')   # 開啟聲音記錄檔
        wf.setnchannels(self.channels)        # 設定聲道
        wf.setsampwidth(audio.get_sample_size(self.sample_format))  # 設定格式
        wf.setframerate(self.rate)              # 設定取樣頻率
        wf.writeframes(b''.join(frames)) # 存檔
        wf.close()
        return b''.join(frames)
    
    def getResponse(self, frame = None):
        frame = frame if frame else self.frame
        client = boto3.client('lexv2-runtime')

        response = client.recognize_utterance(
        botId=self.botId,
        botAliasId=self.botAliasId,
        localeId=self.localeId,
        sessionId=self.sessionId,
        requestContentType="audio/l16; rate=16000; channels=1",
        #responseContentType="text/plain; charset=utf-8",
        inputStream=frame)
        print(response)
        return response

    def update(self):
        frame = self.recording()
        response = self.getResponse(frame)
        messages = self.unzip(response["messages"])
        print(messages)
        inputTranscript = self.unzip(response["inputTranscript"])
        print(inputTranscript)
        audioStream = io.BytesIO(response["audioStream"].read())

        pygame.mixer.music.load(audioStream)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue
        self.quit()

    def quit(self):
        self.game_status.remove("audio")
        self.game_status.remove("action")
        self.game_status.add("implement")