from Functions import *
import numpy as np

animeList = loadList('../animeList.txt')
animeMap = {}

for i in range(len(animeList)) :
    animeMap[animeList[i]] = i

userList = loadList('../userList.txt')

# ratings = np.zeros((len(animeList), len(userList)), dtype=np.int)
ratings = loadCSV('../ratings.csv')
currentRating = int(loadList('../currentRating.txt')[0])

for i in range(currentRating, len(userList)) :
    print "Current user: " + userList[i] + " " + str(i)
    userSoup = readUrl('http://myanimelist.net/malappinfo.php?u='+userList[i]+'&status=all&type=anime', 'xml')
    while userSoup == None:
        time.sleep(10);
        userSoup = readUrl('http://myanimelist.net/malappinfo.php?u='+userList[i]+'&status=all&type=anime', 'xml')

    for anime in userSoup.find_all('anime'):
        # if anime.find('series_status') != None and anime.find('my_score') != None and anime.find('series_animedb_id') != None :
        if anime.find('my_score') != None and anime.find('series_animedb_id') != None :
            # if anime.find('series_status').getText() == '2' and anime.find('my_score').getText() != '0':
            if anime.find('my_score').getText() != '0':
                animeId = anime.find('series_animedb_id').getText()
                if animeId in animeMap:
                    ratings[animeMap[animeId]][i] = int(anime.find('my_score').getText())
                    
    print ratings[:, i]
    if i % 100 == 0:
        print "SAVED " + str(i)
        save('../currentRating.txt', [i])
        np.savetxt("../ratings.csv", ratings.astype(int), fmt='%d', delimiter=",")