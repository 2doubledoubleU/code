import requests
from lxml import html,etree
import ast
import os
import time

runeLookup = {
    "+15-90 Health":"5001",
    "+6 Armor":"5002",
    "+6 Armor or 8 MR (match-up)":"5002",
    "+8 Magic Resist":"5003",
    "+9% Attack Speed":"5005",
    "+10% Attack Speed":"5005",
    "+1-10% ":"5007",
    "+5 AD or 9 AP":"5008",
    "Precision":"8000",
    "Press the Attack":"8005",
    "Lethal Tempo":"8008",
    "Presence of Mind":"8009",
    "Conqueror":"8010",
    "Coup De Grace":"8014",
    "Cut Down":"8017",
    "Fleet Footwork":"8021",
    "Domination":"8100",
    "Relentless Hunter":"8105",
    "Ultimate Hunter":"8106",
    "Electrocute":"8112",
    "Ghost Poro":"8120",
    "Predator":"8124",
    "Cheap Shot":"8126",
    "Dark Harvest":"8128",
    "Ingenious Hunter":"8134",
    "Ravenous Hunter":"8135",
    "Zombie Ward":"8136",
    "Eyeball Collection":"8138",
    "Taste of Blood":"8139",
    "Sudden Impact":"8143",
    "Sorcery":"8200",
    "Transcendence":"8210",
    "Summon Aery":"8214",
    "Nullifying Orb":"8224",
    "Manaflow Band":"8226",
    "Arcane Comet":"8229",
    "Phase Rush":"8230",
    "Waterwalking":"8232",
    "Absolute Focus":"8233",
    "Celerity":"8234",
    "Gathering Storm":"8236",
    "Scorch":"8237",
    "Unflinching":"8242",
    "Nimbus Cloak":"8275",
    "Last Stand":"8299",
    "Inspiration":"8300",
    "Magical Footwear":"8304",
    "Hextech Flashtraption":"8306",
    "Perfect Timing":"8313",
    "Minion Dematerializer":"8316",
    "Future’s Market":"8321",
    "Biscuit Delivery":"8345",
    "Cosmic Insight":"8347",
    "Glacial Augment":"8351",
    "Kleptomancy":"8351",
    "Time Warp Tonic":"8352",
    "Prototype: Omnistone":"8358",
    "Unsealed Spellbook":"8360",
    "Resolve":"8400",
    "Shield Bash":"8401",
    "Approach Velocity":"8410",
    "Conditioning":"8429",
    "Guardian":"8435",
    "Grasp of the Undying":"8437",
    "Aftershock":"8439",
    "Second Wind":"8444",
    "Demolish":"8446",
    "Overgrowth":"8451",
    "Revitalize":"8453",
    "Font of Life":"8463",
    "Bone Plating":"8473",
    "Overheal":"9101",
    "Legend: Bloodline":"9103",
    "Legend: Alacrity":"9104",
    "Legend: Tenacity":"9105",
    "Triumph":"9111",
    "Hail of Blades":"9923"
}

url = "https://runeforge.gg/"

page = requests.get(url)
tree = html.fromstring(page.content)
champions = tree.xpath('//ul[@id="champion-grid-scroll"]/li')

def getRunes(url):
	page = requests.get(url)
	tree = html.fromstring(page.content)
	championName = tree.xpath('//h1[@class="champion-header--title"]/text()')
	primaryRunes = tree.xpath('//a[@class="rune-name"]/text()')
	secondaryRunes = tree.xpath('//a[@class="rune-name drawer-link"]/text()')
	trees = tree.xpath('//h2[@class="rune-name rune-path--name"]/text()')
	extraStats = tree.xpath('//div[@class="stat-shards"]//div[@class="rune-path--rune_description"]/p/text()')
	if extraStats == []:
		extraStats = ['+9% Attack Speed','+5 AD or 9 AP','+6 Armor']	
	while os.path.exists("RunePages/"+ championName[0] + ".txt"):
		championName[0] = championName[0] + str(I)
	with open("RunePages/"+ championName[0] + ".txt", "w") as runeFile:
		runeFile.write('{\"isDeletable\":True,\n\"isEditable\":True,\n\"isValid\":True,\n\"name\":\"AG_' \
			+ championName[0] + '\",\n\"primaryStyleId\":' + runeLookup[trees[0]] + ',\n\"selectedPerkIds\":[' + \
			runeLookup[primaryRunes[0]] + ',\n' + runeLookup[primaryRunes[1]] + ',\n' + runeLookup[primaryRunes[2]] + \
			',\n' + runeLookup[primaryRunes[3]] + ',\n' + runeLookup[secondaryRunes[0]] + ',\n' + \
			runeLookup[secondaryRunes[1]] + ',\n' + runeLookup[extraStats[0]] + ',\n' + runeLookup[extraStats[1]] + \
			',\n' + runeLookup[extraStats[2]] + '],\n\"subStyleId\":' + runeLookup[trees[1]] + '}')
	print("done")
	
if (champions):
	for champion in champions:
		print(champion.attrib.get("data-champion-full"))
		link = champion.xpath('a[@class="champion-loadout-link"]')
		if link:
			getRunes(link[0].attrib['href'])
		else:
			details = champion.xpath('div[@class="champion-modal-open"]')
			builds = details[0].attrib['data-loadouts']
			builds = builds.replace("null","\"\"")
			builds = builds.replace("\\/","/")
			builds = ast.literal_eval(builds)
			for build in builds:
				getRunes(build['link'])
		time.sleep(5)	