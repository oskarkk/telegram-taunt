# arg must be info.taunts
def create(taunts):
    with open('stats.txt', 'a') as f:
        for x in range(len(taunts[1:])):
            f.write(str(x+1) + '\t0\n')

# arg can be a list or a set
def get(tauntList=0):
    with open('stats.txt', 'r') as f:
        content = f.read()
    # deleting a newline at the end
    if content[-1] == '\n': 
        content = content[:-1]
    # split lines to list of 2-element lists
    lines = content.split('\n')
    lines = [ x.split('\t') for x in lines ]
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
    table = stats.get(tauntList)
    table.sort(key=lambda x: x[1], reverse=1)
    table = table[:max]
    return [ i[0] for i in table ]