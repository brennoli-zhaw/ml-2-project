import llm as llModel
import json
from openai import OpenAI
from dotenv import load_dotenv
import os
import cardboardBox as cb
import media as md
from IPython.display import Image, display

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