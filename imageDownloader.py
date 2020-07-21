import praw, requests, os, shutil, unicodedata, json
from unidecode import unidecode

from logic import *

def downloadImage(subredditName): #This function downloads the images from the subreddit
    path = 'images'

    os.mkdir(path)

    url = 'https://www.reddit.com/'

    with open('redditCredentials.json') as f:
        params = json.load(f)

    reddit = praw.Reddit(
        client_id=params['client_id'],
        client_secret=params['api_key'],
        password=params['password'],
        user_agent='<reddit_top> accessAPI:v0.0.1 (by/u/redditUser)',
        username=params['username']
    )

    subreddit = reddit.subreddit(subredditName)

    def deEmojify(inputString):
        returnString = ""

        for character in inputString:
            try:
                character.encode("ascii")
                returnString += character
            except UnicodeEncodeError:
                replaced = unidecode(str(character))
                if replaced != '':
                    returnString += replaced

        return " ".join(returnString.split())  # removes double spaces after replacing an emoji

    name = 0

    for submission in subreddit.hot(limit=100):
        name += 1
        #Replace the invalid characters
        caption = submission.title
        caption = caption.replace(" ", "_")
        caption = caption.replace("'", "-")
        caption = caption.replace(",", "")
        caption = caption.replace("*", "")
        caption = caption.replace("?", "")
        caption = caption.replace("<", "")
        caption = caption.replace("’", "")
        caption = caption.replace("á", "")
        caption = caption.replace("é", "")
        caption = caption.replace("í", "")
        caption = caption.replace("ó", "")
        caption = caption.replace("ú", "")
        caption = caption.replace(">", "")
        caption = caption.replace("<", "")

        if len(caption) > 30:
            caption = caption[0:30] #If the caption is too long, we truncate it

        if name == 51: #we find the first 50 pics
            break
        else:
            url = (submission.url)
            file_name = str(name)
            if url.endswith(".jpg"):
                file_name = caption+".jpg"
                found = True
            elif url.endswith(".png"):
                file_name = caption+".png"
                found = True
            else:
                found = False

            if found == True: #the image is .jpg / .png
                f = open("postedImages.txt","a",encoding="utf-8")
                f.write(file_name+"\n")
                f.close
                imageExists = imageAlreadySaved(file_name)
                if imageExists == False:
                    try:
                        r = requests.get(url)
                        file_name = file_name.replace('"',"")
                        with open(file_name, "wb") as f:
                            f.write(r.content)
                        shutil.move(file_name, path)
                    except FileNotFoundError:
                        print("File not Found!")
                        continue
                    except shutil.Error:
                        print("File already exists!")
                        continue


