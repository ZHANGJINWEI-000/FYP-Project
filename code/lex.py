from settings import *
import boto3
import time

class Lex():
    def __init__(self, game_status, dialog_action, input_action):
        #self.client = boto3.client('lexv2-runtime')
        self.resetInputText()

        self.messages = []

        self.dialog_action = dialog_action
        self.input_action = input_action
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
        self.game_status.add("lex")

    def getMessage(self, text):
        client = boto3.client('lexv2-runtime')

        response = client.recognize_text(
        botId=self.botId,
        botAliasId=self.botAliasId,
        localeId=self.localeId,
        sessionId=self.sessionId,
        text=text)

        print(response)
        try:
            return response["messages"]
        except:
            return []
    
    def resetInputText(self):
        self.setInputText()
    
    def setInputText(self, text = ""):
        print("settext:", text)
        self.inputText = text
    
    def update(self):
        if self.game_status.exist("inchat"):
            return True
        if self.inputText:
            self.messages = self.getMessage(self.inputText)
            self.resetInputText()
            if len(self.messages):
                content = self.convertToDialog()
                self.dialog_action("setup", content)
                self.messages = []
            else:
                self.quit()
        elif self.game_status.exist("entered"):
            inputText = self.input_action("gettext")
            self.setInputText(inputText)
        elif not self.game_status.exist("input"):
            self.input_action("setup")

    def convertToDialog(self):
        content = []
        for message in self.messages:
            content.append({"text":message["content"]})
        return content
    
    def quit(self):
        self.game_status.remove("lex")
        self.game_status.add("action")