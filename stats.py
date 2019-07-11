import pprint
from copy import deepcopy

# create list of taunt IDs and zeros separated by tabs
# arg must be info.taunts
def create(taunts):
    with open('stats.txt', 'a') as f:
        for x in range(len(taunts[1:])):
            f.write(str(x+1) + '\t0\n')

# get list of [id, use_count] for every taunt or selected
# arg can be a list or a set
def get(tauntList=0):
    with open('stats.txt', 'r') as f:
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
    with open('stats.txt', 'w') as f:
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
                    taunts = [],
                    username = []
            ))

            user['count'] += 1
            user['last_use'] = entry['time']

            # add username to the list of user's usernames
            try:
                currentUsername = entry['from']['username']
            except KeyError:
                if user['username']:
                    user['username'] = ['']
                pass
            else:
                if not user['username'] \
                   or user['username'][-1] != currentUsername:
                    user['username'].append(currentUsername)

        self.users = users
        self.various['usersNum'] = len(users)

    def getTaunts(self):
        taunts = {}
        for entry in self.entries:
            id = entry['result_id']

            try:
                taunts[id]
            except KeyError:
                taunts[id] = 1
            else:
                taunts[id] += 1

        self.taunts = taunts
        self.various['usedTaunts'] = len(taunts)

    def __init__(self, filename='chosen.log', start=0):
        self.entries = self.answers(start, filename)
        self.various = { 'uses': len(self.entries) }
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

    def exportTaunts(self, info, sort=0, details=0, filename=0):
        self.various['allTaunts'] = len(info[1:])
        taunts = dict(self.taunts)
        for x in info[1:]:
            try:
                taunts[x['id']]
            except KeyError:
                taunts[x['id']] = 0
            finally:
                if not details:
                    taunts[x['id']] = ( x['id'],
                                        str( taunts[x['id']] ) )
                else:
                    taunts[x['id']] = ( x['id'],
                                        str( taunts[x['id']] ),
                                        x['name'] )

        tauntList = [taunts[x] for x in taunts]

        # sort by id if sort=0, sort by uses and reverse if sort=1
        tauntList.sort(key=lambda x: int(x[sort]), reverse=sort)

        output = '\n'.join([ '\t'.join(taunt) for taunt in tauntList ])
        if filename:
            with open(filename, 'w') as f:
                f.write(output)
        print(output)

#    def exportUsers(self, 
