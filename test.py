from timeit import timeit
import re
import info, textTools as tools

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
      field = tools.clean(taunt[key])
      if f(field, s):
        partMatches.add(index)
        break
  return partMatches


def test(s):
  print(find(s, check))
  print(find(s, check_comp))
  print(find(s, check_dumb))

  print(timeit(lambda: find(s, check), number=100))
  print(timeit(lambda: find(s, check_comp), number=100))
  print(timeit(lambda: find(s, check_dumb), number=100))

test('bedzie was pis')
test('be')
