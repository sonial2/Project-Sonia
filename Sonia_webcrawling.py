# Task 1 
import requests
from bs4 import BeautifulSoup
import pandas as pd 
from pandas import DataFrame
from urllib.request import urlopen as uReq
import unicodedata
import numpy as np
import re
import matplotlib.pyplot as plt

#specify url
url = "http://comp20008-jh.eng.unimelb.edu.au:9889/main/"

#opening connection, grabbing page
uClient = uReq(url)
page_html = uClient.read()
uClient.close()

#parse html and get the file/directory
soup = BeautifulSoup(page_html, "html.parser")

urllist = []
headlinelist = []

for link in soup.findAll('a'):
    firstdirectory = link.get('href')
    
count = 0
# enter the 1st page 
seed_url = url + firstdirectory
urllist.append(seed_url)
subsequentdirectory = ''

# looping over pages 
while count>=0 and firstdirectory != subsequentdirectory: 
    
    if count == 0: 
        seed_url = url + firstdirectory 
        page = requests.get(seed_url)
        soup = BeautifulSoup(page.text, 'html.parser')
        article = soup.find('div', id="mainArticle" )
        headline = article.h1.text
        headlinelist.append(headline)

        #find 2nd link 
        hello = soup.findAll("p",{"class":"nextLink"})
        for stuff in hello: 
            subsequentdirectory = stuff.a["href"]
        count += 1
    else:     
        seed_url = url + subsequentdirectory 
        urllist.append(seed_url)
        # get headline and then write it into the csv file
        page = requests.get(seed_url)
        soup = BeautifulSoup(page.text, 'html.parser')
        article = soup.find('div', id="mainArticle" )
        headline = article.h1.text
        headlinelist.append(headline)

        #find 2nd link 
        hello = soup.findAll("p",{"class":"nextLink"})
        for stuff in hello: 
            subsequentdirectory = stuff.a["href"]
        count += 1
    
# make into a csv file 
df = DataFrame({'Url': urllist, 'Headline': headlinelist})

df.to_csv('task1.csv', index = False) 

# Task 2 
# get names from json file
import itertools
import json
from collections import defaultdict
import string

listofnames = []
compilationnames = []
firstnames = []
lastnames = []
firstplayer = []

with open('tennis.json') as f:
  data = json.load(f)

for files in data: 
    listofnames.append(files['name'].lower())
    
shorternames = []
for name in listofnames:
    var = " ".join([name.split()[0], name.split()[-1]])
    shorternames.append(var)

firstnames = [x.split()[0] for x in listofnames]
lastnames = [x.split()[-1] for x in listofnames]

# get website 
#specify url
url = "http://comp20008-jh.eng.unimelb.edu.au:9889/main/"

#opening connection, grabbing page
uClient = uReq(url)
page_html = uClient.read()
uClient.close()

#parse html and get the file/directory
soup = BeautifulSoup(page_html, "html.parser")

for link in soup.findAll('a'):
    firstdirectory = link.get('href')
# enter the 1st page 
seed_url = url + firstdirectory
subsequentdirectory = ''

count = 0 

# looping over pages 
while count>=0 and firstdirectory != subsequentdirectory: 
    
    if count == 0: 
        seed_url = url + firstdirectory 
        page = requests.get(seed_url)
        soup = BeautifulSoup(page.text, 'html.parser')
        
        # only collect the body of the text 
        article = soup.find('body').text.lower()
        article = re.findall(r"[\w']+|[.,!?;]", article)
        
        # Next part. finding the names within the text. 
        
        wordcount = 0 
        for word in article:
            wordcount += 1
            totallength = len(article)
            if wordcount == totallength:
                compilationnames.append('None') 
                wordcount = 0
            if word in firstnames:
                for word2 in article:
                    if word2 in lastnames:
                        if (word + " " + word2) in shorternames:
                            match.append(word + " " + word2)
                            wordcount = 0
                            break          
            if word in lastnames:
                for word2 in article:
                    if word2 in firstnames:
                        if (word2 + " " + word) in shorternames:
                            compilationnames.append(word + " " + word2)
                            wordcount = 0
                            break 
        firstplayer.append(compilationnames[0])
        compilationnames.clear()

        #find 2nd link 
        hello = soup.findAll("p",{"class":"nextLink"})
        for stuff in hello: 
            subsequentdirectory = stuff.a["href"]
        count += 1
    else:     
        seed_url = url + subsequentdirectory 
        # get headline and then write it into the csv file
        page = requests.get(seed_url)
        soup = BeautifulSoup(page.text, 'html.parser')
        
        # only collect the body of the text 
        article = soup.find('body').text.lower()
        article = re.findall(r"[\w']+|[.,!?;]", article)

        # Next part. finding the names within the text. 
        wordcount = 0 
        for word in article:
            wordcount += 1
            totallength = len(article)
            if wordcount == totallength:
                compilationnames.append('None') 
                wordcount = 0
                break
            if word in firstnames:
                for word2 in article:
                    if word2 in lastnames:
                        if (word + " " + word2) in shorternames:
                            compilationnames.append(word + " " + word2)
                            wordcount = 0
                            break  
            if word in lastnames:
                for word2 in article:
                    if word2 in firstnames:
                        if (word2 + " " + word) in shorternames:
                            compilationnames.append(word2 + " " + word)
                            wordcount = 0
                            break   
        firstplayer.append(compilationnames[0])
        compilationnames.clear()       

        #find 2nd link 
        hello = soup.findAll("p",{"class":"nextLink"})
        for stuff in hello: 
            subsequentdirectory = stuff.a["href"]
        count += 1

# Questions 2a) continued 

longernames = []

for names in listofnames: 
    if len(names.split(" ")) >2 : 
        longernames.append(names)

for findthename in firstplayer: 
    for curlynames in longernames:
        if findthename.split(" ")[0] == curlynames.split(" ")[0] and findthename.split(" ")[-1] == curlynames.split(" ")[-1]:
            firstplayer = [sub.replace(findthename, curlynames) for sub in firstplayer]
        else: 
            continue  

# Question 2b) 

score = []

#specify url
url = "http://comp20008-jh.eng.unimelb.edu.au:9889/main/"

#opening connection, grabbing page
uClient = uReq(url)
page_html = uClient.read()
uClient.close()

#parse html and get the file/directory
soup = BeautifulSoup(page_html, "html.parser")

for link in soup.findAll('a'):
    firstdirectory = link.get('href')
# enter the 1st page 
seed_url = url + firstdirectory
subsequentdirectory = ''

count = 0 

# looping over pages 
while count>=0 and firstdirectory != subsequentdirectory: 
    
    if count == 0: 
        seed_url = url + firstdirectory 
        page = requests.get(seed_url)
        soup = BeautifulSoup(page.text, 'html.parser')

        # only collect the body of the text 
        article = soup.find('body').text.lower()

        if re.search(r"((\d{1,2}[-/]\d{1,2}[\s.,])+|\(\d{1,2}[-/]\d{1,2}\)[.,\s])+", article) == None: 
                        score.append('None')
        else: 
                     score.append((re.search(r"((\d{1,2}[-/]\d{1,2}[\s,.])+|\(\d{1,2}[-/]\d{1,2}\)[\s,.])+", article).group())[:-1])
        
        hello = soup.findAll("p",{"class":"nextLink"})
        for stuff in hello: 
            subsequentdirectory = stuff.a["href"]
        count += 1
    else: 
        seed_url = url + subsequentdirectory 
        # get headline and then write it into the csv file
        page = requests.get(seed_url)
        soup = BeautifulSoup(page.text, 'html.parser')
        
        # only collect the body of the text 
        article = soup.find('body').text.lower()
        if re.search(r"((\d{1,2}[-/]\d{1,2}[\s.,])+|\(\d{1,2}[-/]\d{1,2}\)[.,\s])+", article) == None: 
                        score.append('None')
        else: 
                     score.append((re.search(r"((\d{1,2}[-/]\d{1,2}[\s.,])+|\(\d{1,2}[-/]\d{1,2}\)[\s.,])+", article).group())[:-1])
        # make sure that the max is 7 and not anything above it
        
          #find 2nd link 
        hello = soup.findAll("p",{"class":"nextLink"})
        for stuff in hello: 
            subsequentdirectory = stuff.a["href"]
        count += 1

score = [individual.replace(".", " ") for individual in score]
score = [individual.replace(",", " ") for individual in score]

scorecount = 0 
for value in score: 
    listwithlist = value.split(" ")
    eachvalue = listwithlist[-1]
    if "(" in eachvalue or value == 'None': 
        scorecount += 1
        continue 
    else: 
        diff = int(re.search(r'\d{1,2}', eachvalue).group()) - int(re.search('.*?(\d{1,2})$', eachvalue).group(1))
        if abs(diff) >= 2 and abs(diff) <= 6: 
            scorecount += 1
            continue 
        else: 
            score[scorecount] = 'None'
            scorecount += 1
            
# taking away the single invalid scores
for worder in range(len(score)): 
    if (' ' in score[worder]) == False: 
        score[worder] = 'None'
    else: 
        continue
            
df = DataFrame({'Url': urllist, 'Headline': headlinelist, 'Player': firstplayer, 'Score': score})
df = df[df.Player != 'None']
df = df[df.Score != 'None']

df.to_csv('task2.csv', index = False) 

#Task 3
# get rid of tie breakers 
listofscores = df['Score'].tolist()
newlist = []

for things in listofscores: 
    newlist.append(re.sub(r'\(\d{1,2}[-/]\d{1,2}\)', '', things))

# finding the absolute value
difference = []
absdiff = []
for value in newlist: 
    listwithlist = value.split(" ")
    for eachvalue in listwithlist:
        if eachvalue == '': 
            continue 
        else: 
            diff = int(re.search(r'\d{1,2}', eachvalue).group()) - int(re.search('.*?(\d{1,2})$', eachvalue).group(1))
            difference.append(diff)
    absdiff.append(abs(sum(difference)))
    difference.clear()

# get listof players
col_names_list = df['Player'].tolist()
averagescore = []

#combine the two
from collections import defaultdict
import statistics
dictionaryplayers = defaultdict(list)
for player, score in zip(col_names_list, absdiff):
   dictionaryplayers[player].append(score)  
for key in dictionaryplayers:
    dictionaryplayers[key] = float(statistics.mean(dictionaryplayers[key]))
print(dictionaryplayers)

anotherdf = DataFrame(list(dictionaryplayers.items()),columns = ['player','avg_game_difference']) 
anotherdf.to_csv('task3.csv', index = False) 

#Task 4 
namedictionary = {}
fivevalues = []
from heapq import nlargest 
from numpy import arange
for name in col_names_list: 
    if name in namedictionary:
        namedictionary[name] += 1
    else: 
        namedictionary[name] = 1
fivehighest = nlargest(5, namedictionary, key = namedictionary.get) 
for val in fivehighest: 
    fivevalues.append(namedictionary.get(val))

plt.figure(figsize=((10,8)))
plt.bar(arange(len(fivevalues)),fivevalues)
plt.xticks(arange(len(fivehighest)),fivehighest, rotation=30,)
plt.title("Top 5 player names that articles are most frequently written about")
plt.ylabel("No. of times article written about player")
plt.xlabel("Player names")
plt.savefig("task4.png")
plt.show()

#Task 5 
win_percentage = []
name_written_atleastonce = []
for key in dictionaryplayers.keys():
  name_written_atleastonce.append(key)

with open('tennis.json') as f:
  data = json.load(f)

for name in name_written_atleastonce:
    for i in data:
        if i['name'].lower() == name:
            win_percentage.append(float(i['wonPct'][:-1]))
            
copydf = DataFrame(list(dictionaryplayers.items()),columns = ['player','avg_game_difference']) 
copydf["wonPct"] = win_percentage

fig = plt.figure() 

ax = fig.add_subplot(111)
ax2 = ax.twinx()
width = 0.3

names = name_written_atleastonce
copydf['wonPct'].plot(kind='bar', color='lightsalmon', ax=ax, width=width, position=1, label = "Win percentage", figsize = (20,10))
copydf['avg_game_difference'].plot(kind='bar', color='lightblue', ax=ax2, width=width, position=0, label = "Average game difference", figsize = (20,10))
plt.xticks(arange(len(names)),names, rotation=30)
plt.xlabel("Playernames")
ax.legend(loc = "upper left")
ax2.legend(loc = "upper right")
ax.set_ylabel("Win percentage (%)")
ax2.set_ylabel('Average game difference')
plt.xlabel("Player names")
plt.title("Average game difference and win percentage for each player that at least one article has been written about")
plt.savefig("task5.png", bbox_inches='tight')
