def create():
    x=1
    with open('stats.txt', 'a') as f:
        for x in info.taunts:
            f.write(str(x) + '\t0\n')

def get(tauntList=0):
    with open('stats.txt', 'r') as f:
        content = f.read()
    lines = content.split('\n')
    for line in lines:
        line = line.split('\t')
    if tauntList == 0: return lines
    return [ lines[int(i)-1] for i in tauntList ]

def save(taunt):
    lines = get()
    lines[int(taunt)-1] += 1
    content = '\n'.join( ['\t'.join(line) for line in lines] )
    with open('stats.txt', 'w') as f:
        f.write(content)