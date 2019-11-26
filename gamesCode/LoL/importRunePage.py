import json
import requests
import urllib3
import pickle
import ast

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

try:
	with open('C:\Riot Games\League of Legends\lockfile','r') as file:
		client_string = file.read()
		client_details = client_string.split(":")
except:
	print("game not launched")
	exit(1)

port = client_details[2]
password = client_details[3]

def lolRequest (type,path,package=[]):
	url = "https://127.0.0.1:" + port + path
	if type == "GET":
		response = requests.get(url, auth=("riot", password), verify=False)
	elif type == "POST":
		response = requests.post(url, json=package, auth=("riot", password), verify=False)
	elif type == "DEL":
		response = requests.delete(url, auth=("riot", password), verify=False)
	else:
		input("error")
	return response

currentSummoner = json.loads(lolRequest("GET", "/lol-summoner/v1/current-summoner").text)
summonerID = currentSummoner["summonerId"]

try:
	champSelectInfo = json.loads(lolRequest("GET","/lol-champ-select/v1/session").text)
	for player in champSelectInfo["myTeam"]:
		if player["summonerId"] == summonerID:
			position = player["cellId"]
			break
	for cell in champSelectInfo["actions"]:
		for action in cell:
			if action['actorCellId'] == position and action['type'] == "pick":
				championID = action['championId']
except:
	input("Not in a valid champion select")
	exit(1)

try:
	championName = json.loads(lolRequest("GET", "/lol-champions/v1/inventories/" + str(summonerID) + "/champions/" + str(championID)).text)["name"]
except:
	input("No champion selected")
	exit(1)

try:
	with open("RunePages/"+ championName + ".txt", "r") as runeFile:
		runes = ast.literal_eval(runeFile.read())
except:
	input("No rune page found for " + championName)
	exit(1)

runeBook = json.loads(lolRequest("GET","/lol-perks/v1/pages").text)

for page in runeBook:
	if page['name'].startswith('AG_'):
		lolRequest("DEL","/lol-perks/v1/pages/" + str(page['id']))
		lolRequest("POST","/lol-perks/v1/pages",runes)
		break

input("imported rune page for " + championName)