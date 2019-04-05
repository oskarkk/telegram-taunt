import requests, re
import info, stats, textTools as tools
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
    parts = text.split('&')
    matches = set( range(1,len(info.taunts)) )
    for part in parts:
        partMatches = set()
        for taunt in info.taunts[1:]:
            for key in ['name', 'content', 'category', 'source']:
                t = tools.clean(taunt[key])
                if re.search(r'\b'+part,t):
                    partMatches.add(taunt['id'])
            for voice in taunt['voice']:
                t = tools.clean(voice)
                if re.search(r'\b'+part,t):
                    partMatches.add(taunt['id'])
        matches = matches & partMatches
    return matches

# matches arg is a list
def sendAnswers(query, matches):
    dic = { 'inline_query_id': query,
            'results': []
          }
    for match in matches:
        dicResult = {
            'type': 'voice',
            'id': match,
            'title': match + ' ' + info.taunts[int(match)]['name'],
            'voice_url': httpURL + info.taunts[int(match)]['filename']
#            'caption': match
        }
        dic['results'].append(dicResult)
    print(dic)
    resp = requests.post( 'https://api.telegram.org/bot'
                        + botToken + '/answerInlineQuery', json=dic ).json()
    print(resp)

def sortPopular(matches):
    table = stats.get(matches)
    table.sort(key=lambda x: x[1], reverse=1)
    table = table[:50]
    return [ i[0] for i in table ]

while 1:
    data = getUpdates(botToken, 10)
    while data:
        for update in data:
            if 'inline_query' in update:
                matches = compare(update['inline_query']['query'])
                print(matches)
                sendAnswers(update['inline_query']['id'], sortPopular(matches))
            elif 'chosen_inline_result' in update:
                stats.save(update['chosen_inline_result']['result_id'])
        data = getUpdates(botToken, 10, data[-1])
