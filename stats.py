# arg must be info.taunts
def create(taunts):
    with open('stats.txt', 'a') as f:
        for x in range(len(taunts[1:])):
            f.write(str(x+1) + '\t0\n')

def get(tauntList=0):
    with open('stats.txt', 'r') as f:
        content = f.read()
    # [:-1] for deleting a newline at the end
    lines = content[:-1].split('\n')
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
