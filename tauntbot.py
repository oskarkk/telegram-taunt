import requests
from config import *

def getUpdates(token, timeout=0, lastUpdate=0, types=[], limit=100):
    dic = { 'timeout': timeout,
            'allowed_updates': types,
            'limit': limit
          }

    if lastUpdate:
        dic['offset'] = lastUpdate['update_id'] + 1

    resp = requests.post( 'https://api.telegram.org/bot'
                        + token + '/getUpdates', json=dic ).json()

    print(resp['result'])
    print()
    if resp['result']:
        return resp['result']
    else:
        return 0  # file here

def compare(text):
    return 0

def sendAnswers(query,taunts):
    return 0

def saveStats(taunt):
    pass

while 1:
    data = getUpdates(botToken, 10)
    while data:
        for update in data:
            answers = compare(update['inline_query']['query'])
            chosen = sendAnswers(update['inline_query']['id'], answers)
            saveStats(chosen)
        data = getUpdates(botToken, 10, data[-1])
