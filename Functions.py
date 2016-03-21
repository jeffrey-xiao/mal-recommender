from bs4 import BeautifulSoup
from nltk.downloader import urllib2
import contextlib
import time
import csv
import numpy as np


def loadCSV (filePath, datatype = np.int) :
    with open(filePath,'r') as dest_file:
        data_iter = csv.reader(dest_file, delimiter=",", quotechar='"')
        data = [line for line in data_iter]
    return np.asarray(data, dtype=datatype)

''' 
Returns a set from a file
The items listed in the file must be separated by \n characters
'''
def loadSet (filePath) :
    ret = set()
    for line in open(filePath):
        ret.add(str(line.rstrip('\n')))
    return ret

'''
Returns a list from a file
The items listed in the file must be separated by \n characters
'''

def loadList (filePath) :
    ret = []
    for line in open(filePath):
        ret += [str(line.rstrip('\n'))]
    return ret

'''
Returns a set and list from a file
The items listed in the file must be separated by \n characters
'''
def load (filePath) :
    itemSet = set()
    itemList = []
    for line in open(filePath):
        item = str(line.rstrip('\n'))
        itemSet.add(item)
        itemList += [item]
    return (itemSet, itemList)

'''
Saves a list of items to a file
The items will be separated by \n characters
'''
def save (filePath, itemList) :
    f = open(filePath, 'w+')
    for item in itemList :
        f.write(str(item)+"\n")
    f.close()

'''
Appends an item onto a file
'''

def append (filePath, item) :
    f = open(filePath, 'a')
    f.write(item+"\n")
    f.close()
    
'''
Returns the number of completed and scored anime in animeSet of a specific user
'''
def getCount (user, animeSet):
    userSoup = readUrl('http://myanimelist.net/malappinfo.php?u=' + user + '&status=all&type=anime', 'xml')
    while userSoup == None:
        time.sleep(10);
        userSoup = readUrl('http://myanimelist.net/malappinfo.php?u=' + user + '&status=all&type=anime', 'xml')
        print 'Failed to read http://myanimelist.net/malappinfo.php?u=' + user + '&status=all&type=anime. Retrying.'
    
    cnt = 0
    for anime in userSoup.find_all('anime'):
        if anime.find('series_status') != None and anime.find('my_score') != None and anime.find('series_animedb_id') != None :
            if anime.find('series_status').getText() == '2' and anime.find('my_score').getText() != '0' and anime.find('series_animedb_id').getText() in animeSet:
                cnt += 1
    return cnt

'''
Get the ratings for a specific user for every anime listed in animeList
'''
def getRatings (user, animeList):
    animeMap = {}

    for i in range(len(animeList)) :
        animeMap[animeList[i]] = i
    
    ret = np.zeros(len(animeList))
    
    userSoup = readUrl('http://myanimelist.net/malappinfo.php?u='+user+'&status=all&type=anime', 'xml')
    while userSoup == None:
        time.sleep(10);
        userSoup = readUrl('http://myanimelist.net/malappinfo.php?u='+user+'&status=all&type=anime', 'xml')
    
    for anime in userSoup.find_all('anime'):
        if anime.find('series_animedb_id') != None :
            if anime.find('series_animedb_id').getText() in animeMap:
                ret[animeMap[anime.find('series_animedb_id').getText()]] = anime.find('my_score').getText()
    return ret

'''
Get the name/title of an anime given its id
'''
def getAnimeTitle (animeId) :
    animeSoup = readUrl('http://myanimelist.net/anime/' + str(animeId), 'html.parser')
    while animeSoup == None:
        time.sleep(10);
        print 'Failed to read http://myanimelist.net/anime/' + str(animeId) + '. Retrying.'
    return animeSoup.find('span', {'itemprop' : 'name'}).get_text()

'''
Attempts to read a url. If reading fails, it will return None, otherwise it will return
a Beautiful Soup object
'''
def readUrl (url, parser = 'html') :
    try:
        with contextlib.closing(urllib2.urlopen(url)) as x:
            page = x.read()
            soup = BeautifulSoup(page, parser)
            return soup
    except urllib2.HTTPError:
        print "HTTP Error"
        return None
    except:
        print "ERROR"
        return None

def removeNonAscii(s) : 
    return "".join(i for i in s if ord(i)<128)
