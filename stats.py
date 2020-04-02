import info
import pprint
from datetime import datetime
from copy import deepcopy

# create list of taunt IDs and zeros separated by tabs
# arg must be info.taunts
def create(taunts=info.taunts):
    with open('data/stats.txt', 'a') as f:
        for x in range(len(taunts[1:])):
            f.write(str(x+1) + '\t0\n')

# get list of [id, use_count] for every taunt or selected
# arg can be a list or a set
def get(tauntList=0):
    with open('data/stats.txt', 'r') as f:
        content = f.read()
    # split content to list of 2-element lists
    lines = [ x.split('\t') for x in content.splitlines() ]
    if not tauntList: return lines
    return [ lines[int(i)-1] for i in tauntList ]

# increment use counter of one taunt
def save(taunt):
    lines = get()
    index = int(taunt)-1
    lines[index][1] = str( int(lines[index][1]) + 1 )
    content = '\n'.join( ['\t'.join(line) for line in lines] )
    with open('data/stats.txt', 'w') as f:
        f.write(content)

# sort given ID list by popularity
def sort(tauntList=0, max=50):
    table = get(tauntList)
    table.sort(key=lambda x: int(x[1]), reverse=1)
    # discard everything after <max> most popular taunts
    table = table[:max]
    return [ i[0] for i in table ]

class Stats:

    def answers(self, start, filename):
        with open(filename, 'r') as f:
            lines = list(f)
        answers = []
        for line in lines[-start:]:
            answers.append( eval(line[:-1]) )
        return answers

    def getUsers(self):
        users = {}
        for entry in self.entries:
            id = entry['from']['id']

            user = users.setdefault(id, dict(entry['from'],
                    first_use = entry['time'],
                    count = 0,
                    taunts = {},
                    username = []
            ))

            user['count'] += 1
            user['last_use'] = entry['time']
            result_id = entry['result_id']
            # get use counter for a taunt and increase it by 1,
            # or if it doesn't exist, set it to 0 and increase by 1
            user['taunts'][result_id] = user['taunts'].get(result_id,0) + 1

            # add username to the list of user's usernames
            try:
                currentUsername = entry['from']['username']
            except KeyError:
                if not user['username']:
                    user['username'] = ['']
                pass
            else:
                if not user['username'] \
                   or user['username'][-1] != currentUsername:
                    user['username'].append(currentUsername)

        self.users = users
        self.various['usersNum'] = len(users)

    def getTaunts(self):
        self.various['usedTaunts'] = 0
        for entry in self.entries:
            id = int(entry['result_id'])

            try:
                self.taunts[id]['count']
            except KeyError:
                self.taunts[id]['count'] = 1
                self.various['usedTaunts'] += 1
            else:
                self.taunts[id]['count'] += 1


    def __init__(self, filename='data/chosen.log', tauntList=info.taunts, start=0):
        self.taunts = info.taunts
        self.entries = self.answers(start, filename)
        self.various = {
            'uses': len(self.entries),
            'allTaunts': len(tauntList[1:])
        }
        self.getUsers()
        self.getTaunts()

    def pretty(self, obj): return pprint.pformat(obj, indent=4)

    def print(self, obj, enter=1, userTaunts=0):
        if obj == self.users and userTaunts == 0:
            obj = deepcopy(obj)
            for user in obj:
                del obj[user]['taunts']
        for x in obj:
            print( self.pretty(x), end=': ' )
            if enter: print()
            print( self.pretty(obj[x]) )
            if enter: print()

    def exportTaunts(self, sort=0, details=0, filename=0, min=0):
        outputList = []
        for taunt in self.taunts[1:]:
            count = taunt.get('count',0)
            if count < min: continue
            if details:
                outputList += [ [taunt['id'], count, taunt['name']] ]
            else:
                outputList += [ [taunt['id'], count] ]

        if sort:
            outputList.sort(key=lambda x: x[1], reverse=1)

        for taunt in outputList: taunt[1] = str(taunt[1])

        outputStr = '\n'.join([ '\t'.join(taunt) for taunt in outputList ])
        if filename:
            with open(filename, 'w') as f:
                f.write(outputStr)
        return outputStr

    # useful sort values: 'count', 'last_use'
    def exportUsers(self, sort='count', rev=1, showTaunts=1, max=None):
        users = [ dict(self.users[user]) for user in self.users ]
        users.sort(key=lambda x: x[sort], reverse=rev)

        output = ''

        for user in users[:max]:
            firstUse = datetime.fromtimestamp(user['first_use'])
            lastUse = datetime.fromtimestamp(user['last_use'])
            firstName = user.get('first_name', '')
            lastName = user.get('last_name', '')
            tauntsUsed = len(user['taunts'])
            outputLines = [
                f"{user['id']}: {user['username'][-1]}",
                f"{firstName} {lastName}",
                f"{firstUse}",
                f"{lastUse}",
                f"uses: {user['count']}",
                f"taunts used: {tauntsUsed}"
            ]

            if showTaunts:
                usersTaunts = list(user['taunts'].items())
                usersTaunts.sort(reverse=1, key=lambda x: x[1])
                usersTaunts = usersTaunts[:len(outputLines)]

                for n, taunt in enumerate(usersTaunts):
                    outputLines[n] = f"{outputLines[n]:28.26}" \
                        f"{taunt[1]!s:4.3}" \
                        f"{taunt[0]:5.4}" \
                        f"{self.taunts[int(taunt[0])]['name']:35.35}"
            print('\n'.join(outputLines),'\n')

def getEntriesPastTimestamp(inFilename, outFilename, timestamp):
  count = 0
  with open(outFilename, 'a') as outFile:
    with open(inFilename, 'r') as inFile:
      for x in inFile:
#        print(eval(x)['time'])
        if eval(x)['time'] >= timestamp:
          outFile.write(x)
          count += 1
  print(count)

