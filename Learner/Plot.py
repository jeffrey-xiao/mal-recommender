import matplotlib.pyplot as plt
import numpy as np
import Functions


def displayAllRatings (filePath) :
    ratings = Functions.loadCSV(filePath).astype(int)
    plt.hist(ratings[ratings > 0], 10)
    plt.show()
    

def displayRatings (filePath) :
    ratings = Functions.loadCSV(filePath).astype(int)
    
    for ratingList in ratings:
        plt.hist(ratingList[ratingList > 0], 10)
        plt.show()


# displayRatings('../ratings.csv')

xAxis = [3, 6, 10, 15, 20, 30, 50, 100]
data = [[0.379361387185],
        [0.289807570311],
        [0.43582152675],
        [0.448184327883],
        [0.449458483755],
        [0.442694015648],
        [0.440638545301],
        [0.426895020615]]

plt.plot(np.log(xAxis), data)
plt.show()
