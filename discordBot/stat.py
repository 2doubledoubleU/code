import requests
import json
import sys
import time
import operator
from datetime import datetime
import ast

with open('secrets.txt', 'r') as secretFile:
	secrets = ast.literal_eval(secretFile.read())
	botAuthToken = secrets['botAuthToken']
	guildId = secrets['guildId']

def discordRequest(url,params):
	header = {'Authorization' : 'Bot ' + botAuthToken,'User-Agent' : 'DiscordBot (none, 6)','X-RateLimit-Precision header' : 'millisecond'}
	response = requests.get(url, headers=header, params=params)
	if 'X-RateLimit-Remaining' in response.headers:
		if response.headers['X-RateLimit-Remaining'] == '1':
			print("Pausing so as not to exceed rate limit")
			time.sleep(int(response.headers['X-RateLimit-Reset-After'])+1)	 
	elif not response.status_code == 200:
		print(response.status_code)
		print(response.headers)
		sys.exit("This program exited as a non 200 error code was returned")
	return json.loads(response.content)

details = discordRequest('https://discordapp.com/api/guilds/' + guildId + '/members',{'limit' : '1000'})

#stats = import data from checkinactive.py

for account in details:
	times = datetime.now()-datetime.strptime(account['joined_at'][0:19],'%Y-%m-%dT%H:%M:%S')
	if account['user']['id'] in stats and not times.days == 0:
		if not account['nick'] == None:
			stats[account['nick']] = stats[account['user']['id']]
			del stats[account['user']['id']]
			stats[account['nick']] = stats[account['nick']]/times.days
		else:
			stats[account['user']['username']] = stats[account['user']['id']]
			del stats[account['user']['id']]
			stats[account['user']['username']] = stats[account['user']['username']]/times.days

sorted_stats = sorted(stats.items(), key=operator.itemgetter(1), reverse=True)

for user in sorted_stats:
	print(user[0] + ':' + str(user[1]) + " posts")

'''cutoff = 1
count = 0
for account in details:
	times = datetime.now()-datetime.strptime(account['joined_at'][0:19],'%Y-%m-%dT%H:%M:%S')
	if times.days > cutoff and account['user']['id'] in stats and stats[account['user']['id']] <= 1:
		count +=1
		if not account['nick'] == None:
			print(account['nick'] + " : " + str(stats[account['user']['id']]))
		else:
			print(account['user']['username'] + " : " + str(stats[account['user']['id']]))

print(count)'''