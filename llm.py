from openai import OpenAI
from dotenv import load_dotenv
import os
import validators
import cardboardBox as cb
import json

TEXTMODEL = "gpt-3.5-turbo"
IMGMODEL = "gpt-4o"

#to get startet with the llm model
#create a .env file in the root directory and add the OPENAI_API_KEY
openai_key = ""
load_dotenv()
#automate the process of getting the api key, depending on the system you are running the code
if os.getenv('OPENAI_API_KEY') is None:
    #if you are running the code in google colab
    #im not sure if .env files are supported in google colab
    from google.colab import userdata
    openai_key = userdata.get('OPENAI_API_KEY')
else:
    openai_key = os.getenv('OPENAI_API_KEY')
openaiClient = OpenAI(api_key=openai_key)

    
#here we do some kind of mapping for specific prompts, just to shortcut them, with the drawback of not being able to use the mapping for other prompts
def getSystemPrompt(prompt : str):
    if prompt == "oversee contents":
        return "You oversee what is in the cardboard box. Your goal is, to tell what objects are in the cardboard."
    if prompt == "add or remove object":
        return "You oversee if an object is placed into or taken away from the cardboard box."
    return prompt

#here we do some kind of mapping for specific prompts, just to shortcut them, with the drawback of not being able to use the mapping for other prompts
def getPrompt(prompt : str = None):
    if prompt == "oversee contents":
        #note that this prompt takes data from cb.py
        return f'A series of images is provided to you. You are asked to provide information about what is stored in the cardboard box after the action in the images provided. Before the actions in the images the following was in the box: {cb.getCardboardBoxContents(wantJson = True)}. The JSON structure is as followed: {cb.getObjectInCardboardDescription()} For example: {cb.exampleInCardboardJson()}. If something is added to the cardboard box and its name is already in the object, just increase the quantity, otherwise decrease it or add a new object.'
    if prompt == "add or remove object":
        return f'You get this series of images, which are divided by a white line. You are asked if the action in the image is adding or removing any quantities of objects into or from the cardboard box. Respond in JSON format. The JSON structure is as followed: {cb.getActionDescription()} For example: {cb.exampleActionJson()}.'
    return prompt

def returnJSONAnswerPrompt(originalPrompt : str = None):
    originalPrompt = getPrompt(originalPrompt)
    return f"Answer only in JSON format: {originalPrompt}"

def promptLLM(prompt : str = None, image : str = None, wantJson : bool = False, returnDict : bool = False):
    returnValue = ""
    messages = [{"role": "system", "content" : getSystemPrompt(prompt)}]
    modelToUse = TEXTMODEL
    prompt = getPrompt(prompt)
    #force it to be a json answer prompt
    prompt = prompt if not wantJson else returnJSONAnswerPrompt(prompt)
    messages.append({"role": "user", "content": [{ 
        "type" : "text", 
        "text" : prompt 
    }]})
    if image is not None:
        if not validators.url(image):
            image = f"data:image/jpeg;base64,{image}"
        messages[1]["content"].append({"type": "image_url", "image_url": { "url" : image}})
        modelToUse = IMGMODEL

    if wantJson:
        returnValue = openaiClient.chat.completions.create(
            model=modelToUse,
            max_tokens= 400,
            response_format={ "type": "json_object" },
            messages=messages,
            temperature=0,
            n=1,
        )
    else :
        returnValue = openaiClient.chat.completions.create(
            model=modelToUse,
            messages=messages,
            temperature=0,
            n=1,
        )
    returnValue = returnValue.choices[0].message.content
    if returnDict:
        return json.loads(returnValue)
    return returnValue