from bs4 import BeautifulSoup
from nltk.downloader import urllib2
import socket
import contextlib
import time

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
        f.write(item+"\n")
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
    userSoup = readUrl('http://myanimelist.net/malappinfo.php?u='+user+'&status=all&type=anime', 'xml')
    while userSoup == None:
        time.sleep(10);
        userSoup = readUrl('http://myanimelist.net/malappinfo.php?u='+user+'&status=all&type=anime', 'xml')
    
    cnt = 0
    for anime in userSoup.find_all('anime'):
        if anime.find('series_status') != None and anime.find('my_score') != None and anime.find('series_animedb_id') != None :
            if anime.find('series_status').getText() == '2' and anime.find('my_score').getText() != '0' and anime.find('series_animedb_id').getText() in animeSet:
                cnt += 1
    return cnt

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
