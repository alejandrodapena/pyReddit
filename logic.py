import os
import time
import tweepy
import json
import csv
#This module contains all of the logic operations
def subredditList():
    subreddits = []
    f = open('subreddits.csv', "r")
    lines = f.readlines()
    f.close()
    for i in lines:
        subreddits.append(i.replace("\n",""))
    return subreddits
def imageAlreadySaved(file_name):
    images = os.listdir('images')
    for i in images: #Check if the image is in the folder
        if file_name == i:
            return True
    with open("postedImages.txt","r",encoding="utf-8") as f:
        if file_name in f.read():
            return True

    return False
def getFollowers(profile):
    """
    get a list of all followers of a twitter account
    :param user_name: twitter username without '@' symbol
    :return: list of usernames without '@' symbol
    """
    with open('twitterCredentials.json') as f:
        params = json.load(f)
    consumer_key = params['consumer_key']
    consumer_secret_key = params['consumer_secret_key']
    access_token = params['access_token']
    access_token_secret = params['access_token_secret']


    auth = tweepy.OAuthHandler(consumer_key, consumer_secret_key)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth, wait_on_rate_limit=True)
    ids = []
    for page in tweepy.Cursor(api.followers_ids, screen_name=profile).pages():
        ids.extend(page)
        if len(ids) >= 5000:
            break
    return ids
def followPeople(followerList):
    num = 0
    with open('twitterCredentials.json') as f:
        params = json.load(f)
    consumer_key = params['consumer_key']
    consumer_secret_key = params['consumer_secret_key']
    access_token = params['access_token']
    access_token_secret = params['access_token_secret']

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret_key)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth, wait_on_rate_limit=True)
    for i in followerList:
        try:
            api.create_friendship(i)
            followerList.pop(num)
            num = num +1
            print("FOLLOWING "+str(i))
            time.sleep(60)
            if num == 10:
                break
        except tweepy.error.TweepError:
            print("Already following user "+str(i))
def upload():
    path = 'images'
    files = os.listdir(path)

    with open('twitterCredentials.json') as f:
        params = json.load(f)
    consumer_key = params['consumer_key']
    consumer_secret_key = params['consumer_secret_key']
    access_token = params['access_token']
    access_token_secret = params['access_token_secret']

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret_key)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)
    for f in files:
        if ".jpg" in f or ".png" in f:
            try:
                api.update_with_media("images/"+f)
                print("Posted "+f)
            except tweepy.TweepError: #If the format is not correct or there is an error, program waits and skips that image
                time.sleep(5)
                continue








