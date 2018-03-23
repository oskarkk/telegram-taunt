import sys, json

def pretty(x):
  print(json.dumps(x,indent=2))

# data to parse
dataJson = sys.argv[1]
# what to get from the data
toGet = sys.argv[2]

# convert JSON to Python object
data = json.loads(dataJson)

if toGet == "pretty":
  # format JSON
  pretty(data)  
elif toGet == "update_id":
  # get update ID
  print(data['result'][0]['update_id'])
elif toGet == "inline":
  # get text of the query if there is any
  if 'inline_query' in data['result'][0]:
    print(data['result'][0]['inline_query']['query'])
elif toGet == "inline_id":
  # get ID of the query if there is any
  if 'inline_query' in data['result'][0]:
    print(data['result'][0]['inline_query']['id'])
elif toGet == "if_results":
  # check if there are any results, retur bool
  if data['result']:
    print(1)
  else:
    print(0)
else:
  # if what to get was specified incorrectly
  print("error")
