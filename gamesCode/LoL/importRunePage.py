import json
import requests
import urllib3
import pickle
import ast
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def importRunes():
	try:
		with open('C:\Riot Games\League of Legends\lockfile','r') as file:
			client_string = file.read()
			client_details = client_string.split(":")
			port = client_details[2]
			password = client_details[3]
	except:
		print("game not launched")
		exit(1)

	class lolRequest:
		def __init__(self,port,password):
			self.url = 'https://127.0.0.1:' + port
			self.password = password
			self.auth = ('riot', self.password)
		def get(self, path):
			return requests.get(self.url + path, auth=self.auth, verify=False)

		def post(self, path, data):
			return requests.post(self.url + path, json=data, auth=self.auth, verify=False)

		def delete(self, path):
			return requests.delete(self.url + path, auth=self.auth, verify=False)

	request  = lolRequest(port, password)

	class summoner:
		def __init__(self,json):
			self.details = json
			self.id = self.details['summonerId']

	class championSelect:
		def __init__(self,json):
			self.details = json

		def position(self,id):
			for player in self.details["myTeam"]:
				if player["summonerId"] == id:
					return player["cellId"]
			return None
		def champion(self,id):
			for cell in self.details["actions"]:
				for action in cell:
					if action['actorCellId'] == self.position(id) and action['type'] == "pick":						
						return action['championId']
			print("fuck")
			return None


	summoner = summoner(json.loads(request.get('/lol-summoner/v1/current-summoner').text))
	game = championSelect(json.loads(request.get('/lol-champ-select/v1/session').text))

	print("/lol-champions/v1/inventories/" + str(summoner.id) + "/champions/" + str(game.champion(summoner.id)))

	try:
		championName = json.loads(request.get("/lol-champions/v1/inventories/" + str(summoner.id) + "/champions/" + str(game.champion(summoner.id))).text)["name"]
	except:
		input("No champion selected")
		exit(1)

	try:
		with open("RunePages/"+ championName + ".txt", "r") as runeFile:
			runes = ast.literal_eval(runeFile.read())
	except:
		input("No rune page found for " + championName)
		exit(1)

	runeBook = json.loads(request.get("/lol-perks/v1/pages").text)

	for page in runeBook:
		if page['name'].startswith('AG_'):
			request.delete("/lol-perks/v1/pages/" + str(page['id']))
			request.post("/lol-perks/v1/pages",runes)
			break
	return championName

if __name__ == "__main__":
	champName = importRunes()
	print("imported rune page for " + champName)
	time.sleep(1)