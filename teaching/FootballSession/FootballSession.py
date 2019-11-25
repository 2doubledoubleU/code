import urllib.request
import json

urlData = "https://raw.githubusercontent.com/openfootball/football.json/master/2014-15/en.1.json"
data = urllib.request.urlopen(urlData).read()
jj = json.loads(data.decode('utf-8'))

teamKey = 'arsenal'
Goals = 0

for day in jj['rounds']:
	for match in day['matches']:
		if (match['team1']['key'] == teamKey):
			Goals += match['score1'] 
		elif (match['team1']['key'] == teamKey):
			Goals += match['score2'] 


print(Goals)
