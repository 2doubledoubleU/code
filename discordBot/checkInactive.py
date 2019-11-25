import requests
import json
import sys
import time
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

users = dict()
for account in details:
	id = account['user']['id']
	users[id] = 0

users["deleted"] = 0

def recursiveMessages(channel,id):
	messages = discordRequest('https://discordapp.com/api/channels/' + channel['id'] + '/messages',{'limit' : '100','before':id})
	if messages:
		for message in messages:
				userID = message['author']['id']
				if userID in users:
					users[userID] +=1
				else:
					users["deleted"] +=1
		last = len(messages) - 1
		recursiveMessages(channel,messages[last]['id'])
	else:
		print("done")

url = 'https://discordapp.com/api/guilds/' + guildId + '/channels'
adminChannels = ['593841953163051136']
channels = discordRequest(url,{})
for channel in channels:
	if channel['type'] == 0 and not channel['parent_id'] in adminChannels:
		print("reading " + channel['name'])
		messages = discordRequest('https://discordapp.com/api/channels/' + channel['id'] + '/messages',{'limit' : '100'})
		if messages:
			for message in messages:
				userID = message['author']['id']
				if userID in users:
					users[userID] +=1
				else:
					users["deleted"] +=1
			last = len(messages) - 1
			recursiveMessages(channel,messages[last]['id'])

print(users)