#!/usr/bin/env python
import os
import json
import requests
import uuid
import shutil

#This assumes that you have ffmpeg installed
#sudo apt-get install ffmpeg for me
#you will also need your own username and password
with open('secrets.txt', 'r') as secretFile:
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
redditFeed = input("Reddit feed with the video you want: ")
redditJson = redditFeed + ".json"

session = requests.Session()
customHeaders = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0"}
response = session.get(redditJson,headers=customHeaders)
if response.status_code == 200:
	try: 
		jsonArray = response.json()
		videoLink = jsonArray[0]['data']['children'][0]['data']['secure_media']['reddit_video']['fallback_url']
		videoTitle = jsonArray[0]['data']['children'][0]['data']['title']
		video = videoLink.split("?")[0]
		audio = videoLink.split("/DASH")[0] + "/audio"
	except Exception as e:
		print("Failed to find a reddit video, are you sure it's not hosted on imgur, gfycat, etc?")
		exit(1)


	try:
		with open("video.mp4", "wb") as file:
			vidContent = session.get(video).content
			file.write(vidContent)
			print("Video Saved")
	except Exception as e:
		print("failed to write video: " + str(e))
		exit(1)

	try:
		if session.get(audio).status_code !=200:
				print("No audio found.")
		else:
			with open("audio.mp4", "wb") as file:
				vidContent = session.get(audio).content
				file.write(vidContent)
				print("Audio Saved")
	except Exception as e:
		print("failed to write audio: " + e)
		exit(1)	

	if os.path.exists("audio.mp4"):	
		try:
			convert("video.mp4","audio.mp4",outputFile)
			print("Audio and video combined")
		except Exception as e:
			print("failed to stitch audio/video: " + str(e))
			exit(1)
	else:
		shutil.copy("video.mp4",outputFile)

	with open(outputFile, 'rb') as file:
		print("Uploading...")
		r = session.post("https://api.streamable.com/upload", auth=(userName,passWord), files={videoTitle:file})
		print("Uploaded:")
		print("https://streamable.com/"+ r.json()['shortcode'])
	
	try:
		os.remove("video.mp4")
		os.remove("audio.mp4")
	except:
		coder="lazy"

else:
	print("Reddit returned error code: " + str(response.status_code))
	exit(1)

