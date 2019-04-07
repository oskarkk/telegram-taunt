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

def checkField(field, text):
    t = tools.clean(field)
    if re.search(r'\b'+text,t):
        return 1
    return 0

def compare(query):
    query = tools.clean(query)
    parts = [ x.strip().split(':', maxsplit=1).reverse() for x in query.split('&') ]
    parts = [ [y.strip() for y in x] for x in parts ]

    # get list of ids of all taunts
    matches = set( range(1,len(info.taunts)) )
    
    for part in parts:
        partMatches = set()
        for index, taunt in enumerate(info.taunts[1:], start=1):
            if len(part) == 1:
                for key in ['name', 'content', 'category', 'source']:
                    if checkField(taunt[key], part[0]): partMatches.add(index)
                for voice in taunt['voice']:
                    if checkField(voice, part[0]): partMatches.add(index)
            elif len(part) == 2:
                if part[0] in ['name', 'content', 'category', 'source']:
                    if checkField(taunt[part[0]], part[1]): partMatches.add(index)
                elif part[0] == 'voice':
                    for voice in taunt['voice']:
                        if checkField(voice, part[1]): partMatches.add(index)
        matches &= partMatches
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

while 1:
    data = getUpdates(botToken, 10)
    while data:
        for update in data:
            if 'inline_query' in update:
                matches = compare(update['inline_query']['query'])
                if matches: matches = stats.sort(matches)
                sendAnswers(update['inline_query']['id'], matches)
            elif 'chosen_inline_result' in update:
                stats.save(update['chosen_inline_result']['result_id'])
        data = getUpdates(botToken, 10, data[-1])
