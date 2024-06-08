import llm as llModel
import cardboardBox as cb
import media as md
from IPython.display import Image, display
import os
import json

def showTrainingImages():
    images = md.getTrainingImages(toBase64=False)
    for img in images:
        display(Image(img))

def guessCardboardBoxContent(images, resetCardboardBox = False):
    if resetCardboardBox:
        cb.setEmptyCardboardBox()
    responses = []
    for img in images:
        responses.append(llModel.promptLLM( prompt = "oversee contents", image = md.encodeImage(img), wantJson=True, returnDict=True))
        cb.updateCardboardBoxContentByObject(responses[-1])
    return responses

def compareCardboardBoxContent(images, validData, resetCardboardBox = True):
    responses = guessCardboardBoxContent(images, resetCardboardBox)
    contents = cb.getCardboardBoxContents(wantJson = False)
    contents = json.dumps(order_dict(contents))
    validData = json.dumps(order_dict(json.loads(validData)))
    additionalData =[validData, contents]
    answer = llModel.promptLLM(prompt = "compare contents", additionalData = additionalData, wantJson=True, returnDict=True)
    comparison = {"comparison": answer, "validData": validData, "contents" : contents, "responses": responses}
    return comparison

def order_dict(dictionary):
    return {k: order_dict(v) if isinstance(v, dict) else v
            for k, v in sorted(dictionary.items())}

def compareValidationData():
    os.path.exists("validation/")
    directories = os.listdir("validation/")
    comparisons = []
    for directory in directories:
        if not os.path.isdir("validation/" + directory):
            continue
        images = []
        validData = ""
        files = os.listdir("validation/" + directory)
        for file in files:
            #check length of the file
            if os.path.getsize("validation/" + directory + "/" + file) == 0:
                continue
            if file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith(".png"):
                images.append("validation/" + directory + "/" + file)
            if file.endswith(".json"):
                with open("validation/" + directory + "/" + file, "r") as jsonFile:
                    validData = jsonFile.read()
        comparisons.append(compareCardboardBoxContent(images, validData))
    return comparisons
    