import requests
from config import *

def getUpdates(token, timeout=0, lastUpdate=0, types=[], limit=100):
    dic = { 'timeout': timeout,
            'allowed_updates': types
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
        return 0 # file here

while 1:
    data = getUpdates(botToken, 10)
    while data:
        data = getUpdates(botToken, 10, data[-1])
