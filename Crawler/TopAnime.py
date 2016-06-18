from Functions import *

animeList = []
animeTitles = []

for x in range(0, 1000, 50):
    print x
    soup = readUrl("http://myanimelist.net/topanime.php?limit=" + str(x))
    for link in soup.find_all('a'):
        if link.get('href') != None and link.get('href').startswith('http://myanimelist.net/anime/'):
            animeNum = str(link.get('href').split('/')[4])
            if animeNum.isdigit() and not animeNum in animeList :
                animeList += [animeNum]
                animeTitles += [getAnimeTitle(animeNum)]
                
save('../animeList.txt', animeList)
save('../animeTitles.txt', animeTitles)
