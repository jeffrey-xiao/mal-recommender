from Functions import *
import numpy as np
import Queue as Q

reg = 25
numOfFeatures = 500
x = loadCSV('../features-'+str(numOfFeatures)+'/theta'+str(reg)+'.csv', np.float)

animeTitles = loadList('../animeTitles.txt')
    
pq = Q.PriorityQueue()

for i in range(len(animeTitles)) :
    pq = Q.PriorityQueue()
    for j in range(len(animeTitles)) :
        if i == j :
            continue
        diff = np.sum((x[i, :] - x[j, :]) ** 2)
        pq.put((-diff, j))
        if pq.qsize() > 5 :
            pq.get()
        
    print "Users rated %s, similarly to:" %(animeTitles[i])
    while not pq.empty() :
        print "\t" + animeTitles[pq.get()[1]]
    print ""