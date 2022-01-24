#!/usr/bin/python3 -i

import info
import tauntbot
import textTools

import pprint
from datetime import datetime
from copy import deepcopy
from wcwidth import wcswidth as widelen
import matplotlib.pyplot as plt
import math
from itertools import groupby
from collections import Counter

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

    # parse python objects written to chosen.log, starting at n-th last line
    # TODO: stop usind 'id' as a var name; replace eval with JSON
    def answers(self, start, filename, start_date, end_date):
        with open(filename, 'r') as f:
            lines = list(f)
        answers = []
        start_date = start_date and datetime.fromisoformat(start_date).timestamp()
        end_date = end_date and datetime.fromisoformat(end_date).timestamp()
        for line in lines[-start:]:
            obj = eval(line[:-1])
            date = obj['time']
            if start_date and date < start_date: continue
            if end_date and date > end_date: continue
            answers.append(obj)
        return answers

    def getUsers(self):
        users = {}
        for entry in self.entries:
            id = entry['from']['id']

            user = users.setdefault(id, dict(entry['from'],
                    first_use = entry['time'],
                    use_count = 0,
                    taunt_count = 0,
                    taunts = {},
                    username = []
            ))

            user['use_count'] += 1
            user['last_use'] = entry['time']
            result_id = entry['result_id']

            # increment unique taunt count
            if result_id not in user['taunts']:
                user['taunt_count'] += 1

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


    def __init__(self, filename='data/chosen.log', start=0, start_date=None, end_date=None):
        #self.taunts = info.taunts[:]
        # copy the entire info.taunts, otherwise counts (see getTaunts) will
        # be increased with every instance of Stats
        self.taunts = [info.taunts[0]] + [dict(d) for d in info.taunts[1:]]
        self.entries = self.answers(start, filename, start_date, end_date)
        self.various = {
            'uses': len(self.entries),
            'allTaunts': len(self.taunts[1:])
        }
        self.getUsers()
        self.getTaunts()

    # get pretty formatted string representation of obj
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

    # call with filename only to recreate stats.txt from chosen.log
    # call exportTaunts(sort=1, details=1, num=20) to get short toplist
    def exportTaunts(self, sort=0, details=0, filename=0, min=0, num=None):
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

        # get only the <num> first lines
        if num: outputList = outputList[:num]

        for taunt in outputList: taunt[1] = str(taunt[1])

        outputStr = '\n'.join([ '\t'.join(taunt) for taunt in outputList ])
        if filename:
            with open(filename, 'w') as f:
                f.write(outputStr)
        return outputStr

    # useful sort values: 'use_count', 'last_use'
    def exportUsers(self, sort='use_count', rev=1, showTaunts=1, max=None):
        users = [ dict(self.users[user]) for user in self.users ]
        users.sort(key=lambda x: x[sort], reverse=rev)

        output = ''

        for user in users[:max]:
            firstUse = datetime.fromtimestamp(user['first_use'])
            lastUse = datetime.fromtimestamp(user['last_use'])
            firstName = user.get('first_name', '')
            lastName = user.get('last_name', '')
            # show info about user
            outputLines = [
                f"{user['id']}: {user['username'][-1]}",
                f"{firstName} {lastName}",
                f"{firstUse}",
                f"{lastUse}",
                f"uses: {user['use_count']}",
                f"taunts used: {user['taunt_count']}"
            ]

            # add user's taunt toplist on the right of the info
            if showTaunts:
                usersTaunts = list(user['taunts'].items())
                usersTaunts.sort(reverse=1, key=lambda x: x[1])
                usersTaunts = usersTaunts[:len(outputLines)]
                for n, taunt in enumerate(usersTaunts):
                    # get the correct number of char columns
                    # in the terminal that the string is occupying
                    linelen = widelen(outputLines[n])
                    if linelen > 28:
                        outputLines[n] = outputLines[n][:-linelen+28]
                    else:
                        outputLines[n] += ' ' * (28-linelen)
                    outputLines[n] += "   " \
                        f"{taunt[1]!s:4.3}" \
                        f"{taunt[0]:5.4}" \
                        f"{self.taunts[int(taunt[0])]['name']:35.35}"
            print('\n'.join(outputLines),'\n')

# for chosen.log; useful when you've made a mess with various bot instances
# and want to glue logs into one
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


def year_month(timestamp):
    date = datetime.fromtimestamp(timestamp)
    return f'{date.year}-{date.month:02}'

# TODO: don't split the list? just iterate?
def split_months(start='2019-01-01', end='2022-01-01'):
    entries = Stats(start_date = start, end_date = end).entries
    
    months = {}
    for k, g in groupby(entries, key=lambda x: year_month(x['time'])):
        months.setdefault(k,[]).extend(list(g))

    users_num = []
    uses_num = []
    uses_minus_authors = []
    authors = [138268771, 266306075, 496364629]

    for month in months.values():
        users = {entry['from']['id'] for entry in month}
        users_num.append(len(users))
        uses_num.append(len(month))
        uses_authors = sum(1 for entry in month if entry['from']['id'] in authors)
        uses_minus_authors.append(len(month) - uses_authors)

    return months.keys(), users_num, uses_num, uses_minus_authors

def split_hours(start=None, end=None):
    def get_hour(timestamp):
        return datetime.fromtimestamp(timestamp).hour

    entries = Stats(start_date = start, end_date = end).entries

    hours = [[] for _ in range(24)]
    for k, g in groupby(entries, key=lambda x: get_hour(x['time'])):
        hours[k].extend(list(g))

    authors = [138268771]
    hours_authors = [[entry for entry in hour if entry['from']['id'] in authors] for hour in hours]
    
    uses = [len(hour) for hour in hours]
    uses_authors = [len(hour) for hour in hours_authors]
    uses_minus_authors = [uses[i] - uses_authors[i] for i in range(24)]
    return list(range(24)), uses, uses_minus_authors

def axis(ys, label, color, ticks, divisible):
    if not plt.gca().get_ylabel():
        ax = plt.gca()
    else:
        ax = plt.gca().twinx()
    # rounding up to the int that divided by <ticks> will give number divisible by <divisible>
    grid = math.ceil(max(ys)/ticks/divisible)*ticks*divisible
    ax.set_ylabel(label, color=color, fontweight="bold")
    ax.set_ylim(0, grid*1.1)
    ax.set_yticks([n*grid/ticks for n in range(0,ticks+1)])
    return ax

def plot_months(start='2019-01-01', end='2022-06-01', separate_authors=False):
    labels, users, uses, uses_minus_authors = split_months(start, end)

    plt.xticks(rotation=55, ha='right', va='top')
    plt.subplots_adjust(top=0.85, bottom=0.20, right=0.87)
    plt.grid(linestyle = ':', color = 'lightgray', linewidth = 0.8)
    plt.title('Rozwój TauntBota', pad=20, size='x-large')

    ax1 = axis(users, 'Użytkownicy', 'C0', 5, 5)
    ax2 = axis(uses, 'Użycia', 'C4', 5, 50)

    ax1.plot(labels, users, color='C0', label='użytkownicy bota')
    ax2.plot(labels, uses, color='C4', label='użycia bota')
    if separate_authors:
        ax2.plot(labels, uses_minus_authors, '--', color='C4', label='użycia z wyłączeniem autorów')
        plt.subplots_adjust(bottom=0.23)
        plt.legend(loc='lower center', bbox_transform=plt.gcf().transFigure,
            bbox_to_anchor=(0.5, 0.007), ncol=4, frameon=0)

    ticks = ax1.get_xticks()
    if len(ticks) > 20:
        ax1.set_xticks(ticks[::3])
    elif len(ticks) > 10:
        ax1.set_xticks(ticks[::2])

    filename = f'img/plot-{start}-{end}.png'
    plt.savefig(filename, format='png', dpi=200)
    print(filename)
    plt.close()

def plot_hours(start=None, end=None, separate_authors=False):
    labels, uses, uses_minus_authors = split_hours(start, end)
    plt.subplots_adjust(top=0.85)
    plt.grid(linestyle = ':', color = 'lightgray', linewidth = 0.8)
    plt.title('Użycia TauntBota wg godzin', pad=20, size='x-large')
    
    ax1 = axis(uses, 'Użycia', 'C0', 5, 100)
    ax1.plot(labels, uses, color='C0', label='użycia bota')
    ax1.set_xticks(range(0,24,2))

    if separate_authors:
        ax1.plot(labels, uses_minus_authors, '--', color='C0', label='użycia z wyłączeniem autorów')

    filename = 'img/plot-hours.png'
    plt.savefig(filename, format='png', dpi=200)
    print(filename)
    plt.close()

def plot_oskar():
    labels, uses, uses_minus_authors = split_hours()
    plt.subplots_adjust(top=0.85)
    plt.grid(linestyle = ':', color = 'lightgray', linewidth = 0.8)
    plt.title('Udział Oskara w użyciach TauntBota według godzin', pad=20, size='x-large')
    percents = [(all-others)/all*100 for all, others in zip(uses, uses_minus_authors)]
    ax = plt.gca()
    ax.set_ylabel('% użyć', color='C0', fontweight="bold")
    ax.set_ylim(0, 100)
    ax.plot(labels, percents, color='C0', label='użycia bota')
    ax.set_xticks(range(0,24,2))



    filename = 'img/plot-oskar.png'
    plt.savefig(filename, format='png', dpi=200)
    print(filename)
    plt.close()

# not used
def months_list(start='2021-01', end='2021-12'):
    labels = []
    date_ranges = []

    dates = [int(x) for x in start.split('-') + end.split('-')]
    ym_start = 12*int(dates[0]) + int(dates[1]) - 1
    ym_end = 12*int(dates[2]) + int(dates[3]) - 1

    for ym in range(ym_start, ym_end):
        y, m = divmod(ym, 12)
        this_month = str(y) + '-' + str(m + 1).rjust(2, '0')
        y, m = divmod(ym+1, 12)
        next_month = str(y) + '-' + str(m + 1).rjust(2, '0')
        labels.append(this_month)
        date_ranges.append((this_month,next_month))
    
    return labels, date_ranges

# TODO: check chat types
# TODO: how many of new users don't ever write anything? (remember caching)
def outputlog(n=50, min=0, print_=True):
    answers = []
    wrong = 0
    with open('data/shown.log', 'r') as f:
        for line in f:
            try:
                obj = eval(line[:-1])
                answers.append(obj)
            except:
                wrong += 1
                #print(line)
                continue

    queries = [x['query'] for x in answers if len(x['query']) >= min]
    counted_queries = Counter(queries)

    if print_:
        top_queries = counted_queries.most_common(n)
        print(f'razem: {len(queries)}')
        print(f'unikalnych: {len(counted_queries)}')
        for x in top_queries: print(f'{x[1]}\t{x[0]}')

    return counted_queries

def missed_searches():
    queries = outputlog(min=4, print_=False)
    cleaned = Counter()
    for k, v in queries.items():
        key = textTools.clean(k)
        cleaned.update({key: v})
    
    missed = {query: n for query, n in cleaned.most_common() if not tauntbot.compare(query)}
    return missed

if __name__ == '__main__':
    s = Stats(start=100)
    s.exportUsers(max=10)