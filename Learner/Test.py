from Functions import *
import numpy as np
from scipy import optimize
import time

testList = loadList('../test.txt')

animeList = loadList('../animelist.txt')
anime = len(animeList)

numOfFeatures = 500
x = loadCSV('../theta20.csv', np.float)
animeTheta = np.reshape(x[0:anime * numOfFeatures], (anime, numOfFeatures))

reg = 20.0

ratings = getRatings('jeffreyxiao', animeList)
currRatings = ratings


def getCost (x):
    y = np.array(currRatings)  
    predictedValue = animeTheta.dot(x)

    hasY = np.array(y)
    hasY[hasY != 0] = 1 
    m = len(hasY != 0)

    J = np.sum(((predictedValue - y) ** 2) * hasY) / 2.0 / m
    J += reg / 2.0 * np.sum(x ** 2) / m
    
    return J

def getGradient (x):
    y = np.array(currRatings)
    predictedValue = animeTheta.dot(x)
    
    hasY = np.array(y)
    hasY[hasY != 0] = 1 
    m = len(hasY != 0)

    gradientX = ((predictedValue - y) * hasY).dot(animeTheta) / m
    gradientX += reg * x / m
    return gradientX

def callback (xk) :
    # print optimize.check_grad(getCost, getGradient, xk)
    # print getCost(xk)
    pass
    
correct = 0.0
correct2 = 0.0
correct3 = 0.0
total = 0.0

cnt = 0
for user in testList:
    
    cnt += 1
    ratings = getRatings(user, animeList)
    currRatings = ratings

    
    for i in range(len(ratings)):
        if ratings[i] != 0:
            currRatings = np.array(ratings)
            currRatings[i] = 0
            
            x0 = np.random.rand(numOfFeatures)
            x1 = optimize.fmin_cg(getCost, x0, fprime=getGradient, callback=callback, disp=False)
            
            print "Actual value="+str(ratings[i])+"; Predicted value=" + str(animeTheta.dot(x1)[i])
            diffSquared = (ratings[i] - animeTheta.dot(x1)[i])**2
            print "Diff Squared="+str(diffSquared)
            total += 1
            if diffSquared <= 0.25:
                correct += 1
            if diffSquared <= 1:
                correct2 += 1
            if diffSquared <= 4:
                correct3 += 1
            else :
                print "WRONG " + str(animeList[i])
            print ""
                
    print str(correct) + " " + str(total) + " " + str(cnt)
    print correct / total
    print correct2 / total
    print correct3 / total
    print ""
    if cnt >= 50:
        break
