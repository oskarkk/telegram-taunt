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
                print(taunt[key][index])
        else:
            taunt[key] = [ taunt[key] ]

with open('taunty.csv', 'r') as f:
    x = csv.reader(f, delimiter='\t')
    taunts.append(next(x))
    print(taunts)
    print(len(taunts[0]))
    print(range(len(taunts[0])))
    for row in x:
        taunts.append({ taunts[0][i]: row[i] for i in range(0, len(taunts[0])) })

cellSplit('voice')