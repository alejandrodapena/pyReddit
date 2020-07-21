#@Author: Alejandro Dapena (u/Sarciteu)

#import libraries
import shutil

#import modules
from logic import *
from imageDownloader import *


f = open('profiles.txt', "r")
profiles = f.readlines() #Save the names of the profiles the bot will follow
f.close()
for i in profiles:
    followersList = getFollowers(i)#List of people we will follow
subredditList = subredditList() #List of subreddits the bot will repost
shutil.rmtree('images', ignore_errors=True)
while True:
    for i in subredditList:
        if i != "":
            print("Subreddit: "+i)
            shutil.rmtree('images', ignore_errors=True) #Delete all the images that have been already been posted
            downloadImage(i) #Save our images in local folder 'images'
            upload() #Upload images to our twitter profile
            time.sleep(60)
    time.sleep(60*10) #Wait 10 minutes before following 10 people
    followPeople(followersList)

