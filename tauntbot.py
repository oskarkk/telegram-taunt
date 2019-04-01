import requests
from config import *

def getUpdates(url):
	global updatesNum
	global data 
	data = requests.get(url).json()
	updatesNum = len(data['result'])

getUpdates(tgURL + 'getUpdates?timeout=10')

# tg gives max 100 updates
# get more updates till there are none
def getMoreUpdates():
	while updatesNum > 0 :
		for update in data['result']:
			try:
				# get content of the message
				query = update['inline_query']['query']
			except KeyError:
				# if key doesn't exist, discard update and go to the next update
				continue

		# get the next updates
		lastID = data['result'][-1]['update_id']
		getUpdates( tgURL+'?offset='+str(lastID + 1) )