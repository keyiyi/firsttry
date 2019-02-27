import json

def getTicktes(filename='tickets2.json'):
    with open('tickets2.json', 'r') as f:
        tickets = json.load(f)

    return tickets
