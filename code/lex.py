from settings import *
import boto3
import time

class Lex():
    def __init__(self, game_status, dialog_action, input_action):
        #self.client = boto3.client('lexv2-runtime')
        self.resetInputText()

        self.dialogAction = ""

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
        
        self.dialogAction = ""
        self.game_status.add("lex")
        self.game_status.add("action")

    def getResponse(self, text = None):
        text = text if text else self.inputText
        client = boto3.client('lexv2-runtime')

        response = client.recognize_text(
        botId=self.botId,
        botAliasId=self.botAliasId,
        localeId=self.localeId,
        sessionId=self.sessionId,
        text=text)

        print(response)
        return response

    def getMessage(self, json):
        try:
            return json["messages"]
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
        if self.dialogAction == "Close":
            self.quit()
            return True
        if self.inputText:
            response = self.getResponse()
            messages = self.getMessage(response)
            self.dialogAction = response["sessionState"]["dialogAction"]["type"]
            print(messages, self.dialogAction)
            self.resetInputText()
            if len(messages):
                content = self.convertToDialog(messages)
                self.dialog_action("setup", content)
        elif self.game_status.exist("entered"):
            inputText = self.input_action("gettext")
            self.setInputText(inputText)
        elif not self.game_status.exist("input"):
            self.input_action("setup")

    def convertToDialog(self, messages):
        content = []
        text = ""
        for message in messages:
            text += message["content"] + "\n"
        content.append({"text":text[:-1]})
        return content
    
    def quit(self):
        self.game_status.remove("lex")
        self.game_status.remove("action")
        self.game_status.add("implement")