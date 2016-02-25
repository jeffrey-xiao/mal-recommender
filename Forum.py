from Functions import *

animeSet = loadSet('./animelist.txt')
forumSet = loadSet('./forumPosts.txt')

userList = []
crawled = set()

(crawled, userList) = load('./forumUsers.txt')

cnt = 0
for anime in animeSet:
    animeSoup = readUrl('http://myanimelist.net/forum/?animeid='+anime+'&show='+str(cnt))
    while animeSoup != None:
        for link in animeSoup.find_all('a'):
            if link.get('href') != None and link.get('href').startswith('/forum/'):
                forumId = link.get('href').split('=')[-1] 
                if forumId.isdigit() and link.get('href').split('=')[-2].split('&')[0] == '/forum/?topicid' and forumId not in forumSet:
                    pageCnt = 0;
                    pageSoup = readUrl('http://myanimelist.net/'+link.get('href')+'&show='+str(pageCnt))
                    while pageSoup != None:
                        for pageLink in pageSoup.find_all('a'):
                            if pageLink.get('href') != None and pageLink.get('href').startswith('/profile/'):
                                user = pageLink.get('href').split('/')[2]
                                if not user in crawled:
                                    cnt = getCount(user, animeSet)
                                    if cnt >= 100:
                                        userList += [user]
                                    crawled.add(user)
                                    print str(cnt) + " " + user
        
                        pageCnt += 50
                        pageSoup = readUrl('http://myanimelist.net/'+link.get('href')+'&show='+str(pageCnt))
                    print "Users saved " + link.get('href')
                    forumSet.add(forumId)
                    append('./forumPosts.txt', forumId)
                    save('./forumUsers.txt', userList)
        cnt += 50
        animeSoup = readUrl('http://myanimelist.net/forum/?animeid=5114&show='+str(cnt))
