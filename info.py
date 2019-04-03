import csv

def cellSplit(table, key):
    for row in table[1:]:
        if ';' in row[key]:
            row[key] = row[key].split(';')
            for index, item in enumerate(row[key]):
                row[key][index] = item.strip()
        else:
            row[key] = [ row[key] ]
    return table

def convert(file):
    table = []
    with open(file, 'r') as f:
        x = csv.reader(f, delimiter='\t')
        table.append(next(x))
        for row in x:
            table.append({ table[0][i]: row[i] for i in range(0, len(table[0])) })

    table = cellSplit(table, 'voice')

    for row in table[1:]:
        row['filename'] = row['filename'].replace('.mp3','.ogg').replace(' ','%20')

    return table

taunts = convert('taunty.csv')