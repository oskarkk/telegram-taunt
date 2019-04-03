import requests, textTools as tools
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
    return 0

def sendAnswers(query, matches):
    dic = { 'inline_query_id': query,
            'results': [{
                'type': 'voice',
                'id': 'bbbb',
                'title': 'testtitle',
                'voice_url': httpURL + '801%20Rzadko%20mam%20okazje%20sie%20najebac.ogg',
                'caption': 'aaaa' }]
#               'input_message_content': {'message_text': 'testcontent'} }]
            }
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
                sendAnswers(update['inline_query']['id'], matches)
            elif 'chosen_inline_result' in update:
                saveStats(update['chosen_inline_result']['result_id'])
        data = getUpdates(botToken, 10, data[-1])
