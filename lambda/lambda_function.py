import json
import datetime
import time
import os
import dateutil.parser
import logging
import random
import re

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

Elicit = ["learncodename","b","c"]
Param = [None for i in range(len(Elicit))]
Message = {
    "learncodename": [
        "What rersources do you want to learn?"
    ],
    "b": ["what features of {learncodename} do you want to learn?"],
    "confirm": ["Do you Learn the chatbot in lex?"]
    
}

# reuse client connection as global
#client = boto3.client('lambda')

def try_ex(func):
    try:
        return func()
    except KeyError:
        return None
        
def getSlotsValue(resolvedSlots, slot):
    response = resolvedSlots[slot]["value"]["resolvedValues"][0]
    return response
        
def getMessage(intent_request, e):
    resolvedSlots = intent_request["transcriptions"][0]["resolvedSlots"]
    messageList = Message[e]
    message = messageList[random.randint(0, len(messageList) - 1)]
    slots = re.findall("{(\w+)}", message)
    for slot in slots:
        message = re.sub(f"{{{slot}}}", getSlotsValue(resolvedSlots, slot), message)
    return message
    
def getResponse(dialogAction, intent, message = " ", slotToElicit = None):
    response = {
        "sessionState": {
            "intent": intent,
            "dialogAction": {
                "type": dialogAction
            }
        },
        "messages": [{
            "contentType": "PlainText",
            "content": message
        }]
    }
    #response["sessionState"]["intent"]["state"] = "ReadyForFulfillment "
    if dialogAction == "ElicitSlot":
        response["sessionState"]["dialogAction"]["slotToElicit"] = slotToElicit
    return response

def learn_cloud(intent_request):
    sessionState = try_ex(lambda: intent_request["sessionState"])
    intent = sessionState["intent"]
    nextState = try_ex(lambda: intent_request["proposedNextState"])
    if nextState:
        for ElicitIndex in range(len(Elicit)):
            targetElicit = Elicit[ElicitIndex]
            if nextState["dialogAction"]["slotToElicit"] == targetElicit:
                print(targetElicit, ElicitIndex)
                if ElicitIndex < len(Elicit) - 1:
                    #message = getMessage(intent_request, targetElicit)
                    output = getResponse("Delegate", intent)
                else:
                    print("nn" + ElicitIndex)
                    output = getResponse("ConfirmIntent", intent, "no slot")
                    
    else:            
        output = getResponse("Delegate", intent)
        #output = getResponse("ConfirmIntent", intent, getMessage(intent_request, "confirm"))
    return output
    

# --- Intents ---


def dispatch(intent_request):
    """
    Called when the user specifies an intent for this bot.
    """

    intent_name = intent_request['sessionState']['intent']['name']

    # Dispatch to your bot's intent handlers
    if intent_name == 'learnCode':
        return learn_cloud(intent_request)
    
# --- Main handler ---


def lambda_handler(event, context):
    print(event)
    response = dispatch(event)
    print(response)
    return response

"""
def router(event):
    intent_name = event['sessionState']['intent']['name']
    fn_name = os.environ.get(intent_name)
    print(f"Intent: {intent_name} -> Lambda: {fn_name}")
    if (fn_name):
        # invoke lambda and return result
        invoke_response = client.invoke(FunctionName=fn_name, Payload = json.dumps(event))
        print(invoke_response)
        payload = json.load(invoke_response['Payload'])
        return payload
    raise Exception('No environment variable for intent: ' + intent_name)

def lambda_handler(event, context):
    print(event)
    response = router(event)
    return response
"""