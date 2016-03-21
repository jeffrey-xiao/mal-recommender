from Functions import *
import numpy as np
from scipy import optimize

userList = loadList('../userList.txt')
animeList = loadList('../animeList.txt')
ratings = loadCSV('../ratings.csv')
hasRating = np.array(ratings)
hasRating[hasRating != 0] = 1 

numOfFeatures = 500
reg = 25

numOfTrainingSets = np.count_nonzero(hasRating)

users = len(userList)
anime = len(animeList)

costCache = 0

def getCost (x):    
    X = np.reshape(np.array(x[:anime * numOfFeatures]), [anime, numOfFeatures])
    theta = np.reshape(np.array(x[anime * numOfFeatures : ]), [users, numOfFeatures])
    
    J = np.sum((X.dot(theta.transpose()) - ratings) ** 2 * hasRating) / 2.0 
    J += reg / 2.0 * np.sum(X ** 2) 
    J += reg / 2.0 * np.sum(theta ** 2)
    
    global costCache
    costCache = J
    
    return J

def getGradient (x):
    X = np.reshape(np.array(x[:anime * numOfFeatures]), [anime, numOfFeatures])
    theta = np.reshape(np.array(x[anime * numOfFeatures : ]), [users, numOfFeatures])
    
    gradientX = (((X.dot(theta.transpose())) - ratings) * hasRating).dot(theta) + reg * X
    gradientTheta = (((X.dot(theta.transpose())) - ratings) * hasRating).transpose().dot(X) + reg * theta
    
    return np.concatenate((gradientX.reshape(anime * numOfFeatures), gradientTheta.reshape(users * numOfFeatures)))
    
def callback (xk) :
    global costCache
    print costCache
    
x0 = np.random.rand(users * numOfFeatures + anime * numOfFeatures) / 10

print getCost(x0)

x1 = optimize.fmin_cg(getCost, x0, fprime=getGradient, callback=callback, maxiter=1000)

print "Done minimizing"
print getCost(x1)

np.savetxt("../features-"+str(numOfFeatures)+"/theta"+str(reg)+".csv", x1[0:anime * numOfFeatures], delimiter=",")
    