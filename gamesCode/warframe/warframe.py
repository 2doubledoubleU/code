#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import json, urllib.request

url = "https://n9e5v4d8.ssl.hwcdn.net/repos/weeklyRivensPC.json"
arr = []
pop_count = 0
with urllib.request.urlopen(url) as response:
	for riven in json.loads(response.read().decode()):
		if riven["compatibility"] is None:
			item = riven["itemType"].partition(' ')[0].capitalize() + " Riven (unveiled)"
		elif riven["rerolled"]:
			item = riven["compatibility"].capitalize() + " Riven"
		else:
			item = riven["compatibility"].capitalize() + " Riven (unrolled)"
		arr.append([item, riven["avg"], riven["pop"]])
		pop_count +=riven["pop"]
		
arr = sorted(arr, key=lambda x: x[2], reverse=False)

for row in arr:
	print(row[0]+": "+str("{:,}".format(int(row[1])))+" Plat "+ str(row[2]))
	print(str(row[2]))

print(pop_count)