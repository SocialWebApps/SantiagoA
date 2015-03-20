#-----------------------------------------------#
#Fix the encodding on certain entries
import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
#-----------------------------------------------#
# Accesses the dir that the files are located
# Extracts the files automatically, then decompresses the files
# THen reads the files
# Combines the files

#-----------------------------------------------#
# Accesses the dir that the files are located
# Import the os module, for the os.walk function
#-----------------------------------------------#
import os

# Set the directory you want to start from
rootDir = '.' # change to get direcctory, maybe, but since we are on the same folder
directoryNameDic = {}
fileNameList = []

#Function to check the content of the directory
def printDir(root):
    for dirName, subdirList, fileList in os.walk(root):
        #Creates a dictionary of the File name and Path
        print('Found directory: %s' % dirName)
        for fname in fileList:
            print('\t%s' % fname) 
            
for dirName, subdirList, fileList in os.walk(rootDir):
    #Creates a dictionary of the File name and Path
    path,folder_name = os.path.split(dirName)
    directoryNameDic[folder_name] = dirName

#print "Base Directory"
#printDir(rootDir)

import gzip
import glob
import os.path
# Sets the path based on the dictionary we created earlier
source_dir = directoryNameDic.get("gzFile")
dest_dir = directoryNameDic.get("Data")

#Unconpresses the downloaded data
for src_name in glob.glob(os.path.join(source_dir, '*.gz')):
    base = os.path.basename(src_name)
    dest_name = os.path.join(dest_dir, base[:-3]) + ".txt" 
    with gzip.open(src_name, 'rb') as infile:
        with open(dest_name, 'w') as outfile:
            for line in infile:
                outfile.write(line)
                                   
#print "After Extraction Directory"
#printDir(rootDir)

#Creates a list with the file names
fileNameList =[]
for dirName, subdirList, fileList in os.walk(directoryNameDic.get("Data")):
    for fname in fileList:
        fileNameList.append(fname)

#Prints the fileNameList
#print fileNameList

#Combines the data from all the files into a (very) large file
pathname = directoryNameDic.get("Data") +"/"+"CombinedData.txt" 
with open(pathname, 'w') as outfile:
    for fname in fileNameList:
        pathname = directoryNameDic.get("Data") +"/"+fname  
        #print pathname
        with open(pathname) as infile:
            for line in infile:
                outfile.write(line)

import json
records = [json.loads(line) for line in open(pathname)]

#print json.dumps(records[0], indent=1) # "print" for pretty print

#Create a DataList of 

dataList = []
for index in range(len(records)):
    cord = 0,0

    if 'll' in records[index]:
        cord = (records[index]['ll'][0],records[index]['ll'][1])
    else:
        cord = 'NaN'
    
    if 'hh' in records[index]:
        hh = records[index]['hh']
    if 'r' in records[index]:
        r = records[index]['r']
    if 'u' in records[index]:
        u = records[index]['u']   
    #removes the records that have direct in the r field and only add the bit.ly adress to the List
    if r != 'direct':
        if hh == 'bit.ly':
            data = (hh, r, u, cord)
            dataList.append(data)
            
#--test for duplidates

for index in range(len(dataList)):
#for index in range(30):
        #print dataList_hh[index] + " | " + dataList_r[index] + " | " + dataList_u[index]
    data = dataList[index]
    
    urlToSerch = data[2]
    shortURL = data[1] 
    geoURL = data[3]
    
    #print "Search Index" + str(index)
    print str(index) + " -> " + shortURL + " | " + urlToSerch + " | " + str(geoURL)
    #print dataList[index]


    

#--------Tweeter Search Code------------
import tweepy

API_KEY = 'qtZEaPZt9YaKn5kdvJwG4jbFA'
API_SECRET = 'WE51aaAedTOlt3RiFrXRLAGqkpGt4yHPnYG7wxaLeXk4paKctT'

auth = tweepy.AppAuthHandler(API_KEY, API_SECRET)
  
api = tweepy.API(auth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True)
  
if (not api):
    print ("Can't Authenticate")
    sys.exit(-1)
  
# Continue with rest of code
import sys
import jsonpickle
import os

twitterDataList = []


def twetterSearch(txt,cord):

    searchQuery = txt # this is what we're searching for
    maxTweets = 10000000 # Some arbitrary large number
    tweetsPerQry = 100  # this is the max the API permits
    #fName = 'tweets.txt' # We'll store the tweets in a text file.
 
    # If results from a specific ID onwards are reqd, set since_id to that ID.
    # else default to no lower limit, go as far back as API allows
    sinceId = None
 
    # If results only below a specific ID are, set max_id to that ID.
    # else default to no upper limit, start from the most recent tweet matching the search query.
    max_id = -1L
 
    tweetCount = 0
    print("Downloading max {0} tweets".format(maxTweets))


    #with open(fName, 'w') as f:
        
    while tweetCount < maxTweets:

        try:
            if (max_id <= 0):
                if (not sinceId): new_tweets = api.search(q=searchQuery, count=tweetsPerQry)
                else: new_tweets = api.search(q=searchQuery, count=tweetsPerQry,since_id=sinceId)
            else:
                if (not sinceId): new_tweets = api.search(q=searchQuery, count=tweetsPerQry,max_id=str(max_id - 1))
                else: new_tweets = api.search(q=searchQuery, count=tweetsPerQry,max_id=str(max_id - 1),since_id=sinceId)
                    
            if not new_tweets:
                print("No more tweets found")
                break
            
            tweetCount += len(new_tweets)
#==================
 
            #records = [json.loads(line) for line in open(new_tweets._json)]
            #json.dumps(new_tweets)
            #print len(records)
            #print type(records)
            
            
            #print json.dumps(records[0], indent=1) # "print" for pretty print
            
            #created_at = records[0]['created_at']
            #print created_at
            
            #geo = records[0]['geo']
            
            #if geo is not 'none':
            #    print "NO cords"
            #else:
            #    print "geo" + geo
#==================
            data = (tweetCount, searchQuery,cord)
            twitterDataList.append(data)
            
            #f.write(str(twitterDataList) + '\n') # wirtes the result to a txt file
            
            
            #print("Downloaded {0} tweets".format(tweetCount))
            max_id = new_tweets[-1].id
            
        except tweepy.TweepError as e:
            # Just exit if any error
            print("some error : " + str(e))
            break
#---------------------------------------

#for index in range(len(dataList)):
for index in range(10):
        #print dataList_hh[index] + " | " + dataList_r[index] + " | " + dataList_u[index]
    data = dataList[index]
    
    urlToSerch = data[2]
    shortURL = data[1]
    cord = data[3]
    
    print "Search Index" + str(index)
    twetterSearch(urlToSerch, cord)
    #print str(index) + " -> " + shortURL + " | " + urlToSerch
    #print dataList[index]



for index in range(len(twitterDataList)):
        #print dataList_hh[index] + " | " + dataList_r[index] + " | " + dataList_u[index]
    data = twitterDataList[index]
    
    print "index: " + str(index) + " -> " + str(data[0]) + " | " + str(data[1]) + " | " + str(data[2])