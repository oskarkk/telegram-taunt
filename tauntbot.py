#!/usr/bin/python -u

import requests, re, time, os
import info, stats, textTools as tools
from config import *

# little setup
if not os.path.exists('data'):
    os.makedirs('data')

# return list of results or 0 if there are none
def getUpdates(token, timeout=0, lastUpdate=0,
               types=['inline_query','chosen_inline_result'], limit=100):
    dic = { 'timeout': timeout,
            'allowed_updates': types,
            'limit': limit
          }

    # "An update is considered confirmed as soon as getUpdates is called 
    # with an offset higher than its update_id."
    if lastUpdate:
        dic['offset'] = lastUpdate['update_id'] + 1

    resp = requests.post( 'https://api.telegram.org/bot'
                        + token + '/getUpdates', json=dic ).json()

    print(resp)

    if 'result' in resp:
        return resp['result']
    else:
        if resp['ok'] != True:
            # write errors to a file
            with open('data/error.log', 'a') as f:
                f.write(str(dic)+'\n'+str(resp)+'\n\n')
        return 0

def compositeSearch(query):
    # split composite queries, strip whitespace around '&'
    # and make list of ['key', 'searched string'] or just ['searched string']
    parts = [ x.strip().split(':', maxsplit=1) for x in query.split('&') ]
    # reverse any ['key', 'searched string'] to ['searched string', 'key']
    # and strip whitespaces inside
    parts = [ [y.strip() for y in x][::-1] for x in parts ]

    # get list of ids of all taunts
    matches = set( range(1,len(info.taunts)) )
    
    # if query is empty, return all taunts
    if not query:
        return matches

    # helper function for matching info fields and query
    def check(field):
        t = tools.clean(field)
        return re.search(r'\b'+part[0], t)

    # I am deeply sorry for this symphony of fors and ifs
    for part in parts:
        # make set for all matches for a part
        partMatches = set()
        for index, taunt in enumerate(info.taunts[1:], start=1):
            # part without searching in key
            if len(part) == 1:
                for key in ['name', 'content', 'category', 'source']:
                    if check(taunt[key]): 
                        partMatches.add(index)
                        break
                else:
                    for voice in taunt['voice']:
                        if check(voice): 
                            partMatches.add(index)
                            break
            # part with key in part[1]
            elif len(part) == 2:
                if part[1] in ['name', 'content', 'category', 'source']:
                    if check(taunt[part[1]]): partMatches.add(index)
                elif part[1] == 'voice':
                    for voice in taunt['voice']:
                        if check(voice): 
                            partMatches.add(index)
                            break
        # none matches in any part mean that nothing will match overall
        if not partMatches:
            return []
        # set intersection
        matches &= partMatches
    return matches

# compare query with info.taunts and return list of taunt IDs
def compare(query):
    query = tools.clean(query)

    for egg in easterEggs:
        if query == egg[0]: return [ egg[1] ]

    # searching by ID, only if query is a number
    try:
        num = int(query)
    except ValueError:
        pass
    else:
        # check if given number is <= than number of taunts
        tauntsNum = len(info.taunts[1:])
        if num <= tauntsNum:
            return list( range(num, min(num+50,tauntsNum+1)) )

    # find matching taunts by string comparison and sort them by popularity
    matches = compositeSearch(query)
    if matches: matches = stats.sort(matches)
    return matches

# matches arg is a list of taunt IDs
def sendAnswers(query, matches):
    dic = { 'inline_query_id': query,
            'cache_time': 30,
            'results': []
    }
    for match in matches:
        dicResult = {
            'type': 'voice',
            'id': str(match),
            'title': str(match) + ' ' + info.taunts[int(match)]['name'],
            'voice_url': httpURL + info.taunts[int(match)]['filename']
#            'caption': match
        }
        dic['results'].append(dicResult)
    resp = requests.post( 'https://api.telegram.org/bot'
                        + botToken + '/answerInlineQuery', json=dic ).json()
    print(resp)

def run():
    updatesList = getUpdates(botToken, 10)
    # tg gives max 100 updates, so repeat until there are none left
    while updatesList:
        for update in updatesList:
            # when someone is requesting taunts from the bot
            if 'inline_query' in update:
                matches = compare(update['inline_query']['query'])
                sendAnswers(update['inline_query']['id'], matches)
            # when tg informs the bot that someone has chosen a taunt
            # (for every result there may or may not be an associated query,
            # remember caching)
            elif 'chosen_inline_result' in update:
                # increment use counter of particular taunt
                stats.save(update['chosen_inline_result']['result_id'])
                # save results to file for future processing
                with open('data/chosen.log', 'a') as f:
                    update['chosen_inline_result']['time'] = int(time.time())
                    f.write(str(update['chosen_inline_result'])+'\n')
        # get the next updates, at the same time confirming updates with id
        # lower than id of the last update in updatesList
        updatesList = getUpdates(botToken, 10, updatesList[-1])

# main loop
if __name__ == "__main__":
    while True:
        try:
            run()
        except ConnectionError:
            sleep(10)
            continue
