import csv

# convert csv (actually tab-separated) file to convenient object
def convert(file):
    table = []
    with open(file, 'r') as f:
        x = csv.reader(f, delimiter='\t')
        # first row - list of column headers
        table.append(next(x))
        # rest of the rows - dicts in form 'column_header': cell
        for row in x:
            table.append({ table[0][i]: row[i] for i in range(0, len(table[0])) })

    # function in case of possible new splitable columns in the future
    def cell_split(table, key):
        for row in table[1:]:
            row[key] = [ x.strip() for x in row[key].split(';') ]
        return table

    # split every cell in voice column to list of single voices
    table = cell_split(table, 'voice')

    # replace audio extension and prepare for passing as url
    for row in table[1:]:
        row['filename'] = row['filename'].replace('.mp3','.ogg').replace(' ','%20')

    return table

taunts = convert('data/taunty.csv')
