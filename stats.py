# arg must be info.taunts
def create(taunts):
    with open('stats.txt', 'a') as f:
        for x in range(len(taunts[1:])):
            f.write(str(x+1) + '\t0\n')

# arg can be a list or a set
def get(tauntList=0):
    with open('stats.txt', 'r') as f:
        content = f.read()
    # split content to list of 2-element lists
    lines = [ x.split('\t') for x in content.splitlines() ]
    if not tauntList: return lines
    return [ lines[int(i)-1] for i in tauntList ]

def save(taunt):
    lines = get()
    index = int(taunt)-1
    lines[index][1] = str( int(lines[index][1]) + 1 )
    content = '\n'.join( ['\t'.join(line) for line in lines] )
    with open('stats.txt', 'w') as f:
        f.write(content)

def sort(tauntList=0,max=50):
    table = get(tauntList)
    table.sort(key=lambda x: x[1], reverse=1)
    table = table[:max]
    return [ i[0] for i in table ]