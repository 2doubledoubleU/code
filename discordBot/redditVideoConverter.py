#!/usr/bin/env python
import os
import json
import requests
import uuid
import shutil
import ast
from lxml import html,etree
import time

def videoConvert(redditFeed):
	#This assumes that you have ffmpeg installed
	#sudo apt-get install ffmpeg for me
	#you will also need your own username and password
	with open('redditVideoConverter.secret', 'r') as secretFile:
			secrets = ast.literal_eval(secretFile.read())
			userName = secrets['userName']
			passWord = secrets['passWord']

	if os.path.exists("audio.mp4"):
		os.remove("audio.mp4")

	if os.path.exists("video.mp4"):
		os.remove("video.mp4")

	def convert(video,audio,output):
		os.system("ffmpeg -i " + video + " -i " + audio + " -c copy " + output + " -y > /dev/null 2>&1")

	outputFile = str(uuid.uuid4()) + ".mp4"
	redditJson = redditFeed + ".json"

	session = requests.Session()
	customHeaders = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0"}
	response = session.get(redditJson,headers=customHeaders)
	try: 
		jsonArray = response.json()
		videoLink = jsonArray[0]['data']['children'][0]['data']['secure_media']['reddit_video']['fallback_url']
		videoTitle = jsonArray[0]['data']['children'][0]['data']['title']
		video = videoLink.split("?")[0]
		audio = videoLink.split("/DASH")[0] + "/audio"

		with open("video.mp4", "wb") as file:
			vidContent = session.get(video).content
			file.write(vidContent)

		if session.get(audio).status_code ==200:
			with open("audio.mp4", "wb") as file:
				vidContent = session.get(audio).content
				file.write(vidContent)

		if os.path.exists("audio.mp4"):	
			convert("video.mp4","audio.mp4",outputFile)
		else:
			shutil.copy("video.mp4",outputFile)

		with open(outputFile, 'rb') as file:
			r = session.post("https://api.streamable.com/upload", auth=(userName,passWord), files={videoTitle:file})
		
		convertedLink = "https://streamable.com/"+ r.json()['shortcode']
		
		wait = 1
		while wait < 8:
			response = session.get(convertedLink,headers=customHeaders)
			tree = html.fromstring(response.content)
			if tree.xpath('//div[@id="play-button"]'):
				break
			else:
				time.sleep(wait)
				wait += 1

		return convertedLink

	except Exception as e:
			exit(1)

if __name__ == "__main__":
	redditFeed = input("Reddit feed with the video you want: ")
	result = videoConvert(redditFeed)
	input(result)
