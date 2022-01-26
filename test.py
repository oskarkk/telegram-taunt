from timeit import timeit
import cProfile

import re

import info
import textTools as tt
import tauntbot
import stats


strings = ['a', 'b', 'Zażółć gęślą jaźń', 'jeszcze', 'be', 'tak jak pan jezus powiedzial', 
        'dobry wieczor', 'ąśćóódsf', 'ąśćóódsfafwepiscvkmmkvpwoekapdvasdvas', 'będziemy jechac'
]


# original function before 2020-01
def check(t, s):
    return re.search(r'\b'+s, t)

# function with compiled regex
def check_comp(t, s):
    return s.search(t)

# more efficient without regex
def check_dumb(t, s):
    if t.startswith(s) or ' '+s in t:
        return True
    return False

def find(s, f):
    if f is check_comp:
        s = re.compile(r'\b'+s)
    partMatches = set()
    for index, taunt in enumerate(info.taunts[1:], start=1):
        for key in ['name', 'content', 'category', 'source']:
            field = tt.clean(taunt[key])
            if f(field, s):
                partMatches.add(index)
                break
    return partMatches


def test_find(s):
    
    def test(f):
        for s in strings:
            test_find(s)

    for f in (check, check_comp, check_dumb):
        print(timeit(lambda: test(s, f), number=100))
        print(timeit(lambda: test(s, f), number=100))
        print(timeit(lambda: test(s, f), number=100))


def test2():
    for s in strings:
        print(timeit(lambda: tauntbot.compare(s), number=100))


def profile():
    cProfile.run('test2()', sort='cumtime')


def test_clean():
    for s in strings:
        for f in (tt.clean, tt.clean_legacy):
            print(timeit(lambda: f(s), number=50000))


def test_queries():
    queries = [q for q in stats.query_log() if q]
    for query in queries:
        tauntbot.compare(query)