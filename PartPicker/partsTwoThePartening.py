import requests
from bs4 import BeautifulSoup
import pandas as pd

def makeSoup(url):
	page = requests.get(url)
	soup = BeautifulSoup(page.content, 'html.parser')
	return soup

base_url = "https://www.malpasonline.co.uk"
search_url = "/s/c/tractor-parts/?Sort=1&Page="

originalPageSoup = makeSoup(base_url + search_url + str(2))
lastPageLink = originalPageSoup.find("a",{"id":"ctl00_content_FullWidth_gvResults_ctl33_aLastPage"})['href']
lastPageNumber = int(lastPageLink.split("=")[2])
lastPageNumber = 732
parts = []

for page in range(732,lastPageNumber+1,1):
	print("\r", end='')
	print("page " + str(page+1) + " of " + str(lastPageNumber+1), end='', flush=True)
	soup = makeSoup(base_url + search_url + str(page))
	part = soup.findAll("div",{"class","Part_Details"})
	for each in part:
		partNumber = each.find("div",{"class","Part_Number"}).find("a").text
		description = each.find("div",{"class","Part_Desc"}).find("a").text.strip()
		partURL = base_url + each.find("div",{"class","Part_Desc"}).find("a")['href']
		partSoup = makeSoup(partURL)
		techInfoRow = partSoup.findAll("td",{"class","pa-att-name"})
		techInfo = dict()
		for row in techInfoRow:
			techInfo[row.text] = row.find_next_sibling("td").text
		try:
			modelBrands = partSoup.find("table",{"class","compatible_model_results"}).findAll('th')
			models = dict()
			for model in modelBrands:
				modelLinks = model.find_next("td").findAll("a")
				for link in modelLinks:
					models[model.text] = link.text
		except:
			models = "None"
		try:
			partNosBrands = partSoup.find("table",{"class","part_Number_results"}).findAll('th')
			partNos = dict()
			for partNo in partNosBrands:
				partNos[partNo.text] = [link.text for link in partNo.find_next("td").findAll("a")]
		except:
			partNos = "None"

		parts.append([partNumber, description, techInfo, models, partNos])

df = pd.DataFrame(parts,columns=['Part_Number','Description','Technical_Information','Models','Manufacturer_Part_Numbers'])
df.to_csv("test.csv")
