from Functions import *

animeList = [31964, # Boku no Hero Academia 
             31804, # Girl Meets Bear
             31933, # JoJo Part 4
             32542, # Sakamoto
             32438, # Mayoiga
             31405, # Joker Game
             31478, # Bungou Stray Dogs
             28623, # Iron Fortress
             31376  # Flying witches
            ]

for anime in animeList :
    soup = readUrl("http://myanimelist.net/anime/" + str(anime))
    print soup.find('span', {'itemprop': 'name'}).text.strip()
    print soup.find('div', {'class': 'fl-l score'}).text.strip()
    print soup.find('span', {'class': 'members'}).text.strip().split(" ")[1]
    print "";