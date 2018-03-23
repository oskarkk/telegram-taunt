import sys, json

# file arguments
inline_id = int(sys.argv[1])
query = sys.argv[2]
url = sys.argv[3]
filenamesString = sys.argv[4]

# list of all files
filenames = filenamesString.split('\n')
# list for files matching inline query
results = []

for filename in filenames:
  # title is the part of the filename before ".mp3"
  title = filename.split('.')[0]
  # check if title matches inline query (case insensitive)
  if query.lower() in title.lower():
    # first "word" of the filename is the taunt number
    number = int(filename.split()[0])
    # prepare JSON object
    results.append({'type': 'audio', 'id': number, 'audio_url': url+filename.replace(' ','%20'), 'title': title})

# for debug
#print(filenames)
#print(results)

# if there are any matches prepare and return full JSON answer
if results:
  answers = {'inline_query_id': inline_id, 'results': results[0:9]}
  print(json.dumps(answers))
