import json
import copy

itemsInCardBoard = {"objects" : []}

def exampleInCardboardJson():
    return '{"objects": [{"name": "apple", "quantity": "5"}]}'

def getObjectInCardboardDescription():
    return "{ objects: [ name: 'give the object a name' ,  quantity: 'quantity of object in cardbox']}"

def exampleActionJson():
    return '{"objects": [{"name": "apple", "isAdded": "True", "quantity": "5"}]}'

def getActionDescription():
    return "{ objects: [ name: 'give the object a name' ,  isAdded: 'True if object is added, False if object is removed', quantity: 'quantity of objects related to the adding or removing action']}"

def getCardboardBoxContents(wantJson = False):
    global itemsInCardBoard
    if wantJson:
        return json.dumps(itemsInCardBoard)
    return itemsInCardBoard

def setEmptyCardboardBox():
    global itemsInCardBoard
    itemsInCardBoard = {"objects" : []}

def getCardboardBoxContents(wantJson = False):
    global itemsInCardBoard
    if wantJson:
        return json.dumps(itemsInCardBoard)
    return itemsInCardBoard

#we do some type corrections and allow strings as quantity, since it is not clear if the llm will return a string or an int
def updateCardboardBoxContentByName(name : str, quantity : str | int):
    global itemsInCardBoard
    if "objects" not in itemsInCardBoard:
        itemsInCardBoard["objects"] = []
    else: 
        items = itemsInCardBoard["objects"] 
        for value in items:
            if value["name"] == name:
                if int(quantity) <= 0:
                    itemsInCardBoard["objects"].remove(value)
                    return
                if "quantity" not in value:
                    value["quantity"] = quantity
                    return
                value["quantity"] = int(quantity)
                return
    itemsInCardBoard["objects"].append({"name": name, "quantity": int(quantity)})

def updateCardboardBoxContentByObject(object : dict):
    global itemsInCardBoard
    itemsInCardBoard["objects"] = copy.deepcopy(object["objects"])

def removeCardboardBoxContentByName(name : str):
    global itemsInCardBoard
    if "objects" not in itemsInCardBoard:
        return
    items = itemsInCardBoard["objects"]
    for value in items:
        if value["name"] == name:
            itemsInCardBoard["objects"].remove(value)
            return
        
def removeCardboardBoxContentByObject(object : dict):
    list = object["objects"]
    for value in list:
        removeCardboardBoxContentByName(value["name"])


def addQuantityToCardboardBoxContentByName(name : str, quantity : str | int):
    global itemsInCardBoard
    if "objects" not in itemsInCardBoard:
        itemsInCardBoard["objects"] = []
    else: 
        items = itemsInCardBoard["objects"] 
        for value in items:
            if value["name"] == name:
                if "quantity" not in value:
                    value["quantity"] = quantity
                    return
                value["quantity"] = int(value["quantity"]) + int(quantity)
                return
    itemsInCardBoard["objects"].append({"name": name, "quantity": int(quantity)})

def addQuantityToCardboardBoxContentByObject(object : dict):
    list = object["objects"]
    for value in list:
        addQuantityToCardboardBoxContentByName(value["name"], value["quantity"])