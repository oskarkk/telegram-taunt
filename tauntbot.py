import requests, re
import info, textTools as tools
from config import *

def getUpdates(token, timeout=0, lastUpdate=0,
               types=['inline_query','chosen_inline_result'], limit=100):
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
    text = tools.clean(text)
    print(text)
    matches = set()
    for taunt in info.taunts[1:]:
        for key in ['name', 'content', 'category', 'source']:
            t = tools.clean(taunt[key])
            if re.search(r'\b'+text,t):
                matches.add(taunt['id'])
        for voice in taunt['voice']:
            t = tools.clean(voice)
            if re.search(r'\b'+text,t):
                matches.add(taunt['id'])
    return matches

def sendAnswers(query, matches):
    dic = { 'inline_query_id': query,
            'results': []
          }
    for match in matches:
        dicResult = {
            'type': 'voice',
            'id': match,
            'title': match + ' ' + info.taunts[match]['name'],
            'voice_url': httpURL + info.taunts[match]['filename'],
            'caption': match
        }
        dic['results'].append(dicResult)
    print(dic)
    resp = requests.post( 'https://api.telegram.org/bot'
                        + botToken + '/answerInlineQuery', json=dic ).json()
    print(resp)

def saveStats(taunt):
    pass

while 1:
    data = getUpdates(botToken, 10)
    while data:
        for update in data:
            if 'inline_query' in update:
                matches = compare(update['inline_query']['query'])
                print(matches)
                sendAnswers(update['inline_query']['id'], matches)
            elif 'chosen_inline_result' in update:
                saveStats(update['chosen_inline_result']['result_id'])
        data = getUpdates(botToken, 10, data[-1])
