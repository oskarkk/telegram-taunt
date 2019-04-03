import csv, pprint

printer = pprint.PrettyPrinter(indent=4)
pp = printer.pprint

taunts = []

def cellSplit(key):
    for taunt in taunts[1:]:
        if ';' in taunt[key]:
            taunt[key] = taunt[key].split(';')
            for index, item in enumerate(taunt[key]):
                taunt[key][index] = item.strip()
        else:
            taunt[key] = [ taunt[key] ]

with open('taunty.csv', 'r') as f:
    x = csv.reader(f, delimiter='\t')
    taunts.append(next(x))
    for row in x:
        taunts.append({ taunts[0][i]: row[i] for i in range(0, len(taunts[0])) })

cellSplit('voice')

for taunt in taunts[1:]:
    taunt['filename'] = taunt['filename'].replace('.mp3','.ogg').replace(' ','%20')
