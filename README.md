# Mal-Recommender

## Description

Mal Recommender is a recommender system for predicting MyAnimeList scores using linear regression.

Under the Crawler package are some files for crawling data on top anime, and users. I specifically chose the top 1000 anime and
users who have watched more than 100 of the top 1000. The MyAnimeList API did not have any tools for finding users, so I repeatedly 
crawled the recently active page and specific anime forums to get 10,000 users. In total, I had approximately 2 million data points
and a 1000x10000 table describing the ratings which was 20% fill.

Under the Learner package are the programs to both plot, learn, and test the data. I created another cross validation data set of
approximately 1000 users to determine the linear regularization parameter and the number of features to use. Finally, I used a testing data set
of approximately 1000 users to determine the final accurancy of the predictor.

## Results

Top row is regularization parameter.

### 500 Features
|                 | 3       | 6       | 10      | 15      | 20      | 30      | 50      | 100     |
|-----------------|---------|---------|---------|---------|---------|---------|---------|---------|
| Score Diff = 0  | 0.37936 | 0.28980 | 0.43582 | 0.44818 | 0.44945 | 0.44269 | 0.44063 | 0.42689 |
| Score Diff <= 1 | 0.66282 | 0.52252 | 0.72763 | 0.73624 | 0.73773 | 0.72890 | 0.72396 | 0.70461 |
| Score Diff <= 2 | 0.91816 | 0.75100 | 0.94533 | 0.94998 | 0.94871 | 0.94417 | 0.93973 | 0.92715 |

### 1000 Features
|                 | 10      | 15      | 30      | 60      |   
|-----------------|---------|---------|---------|---------|   
| Score Diff = 0  | 0.44900 | 0.44996 | 0.43627 | 0.40715 |
| Score Diff <= 1 | 0.73246 | 0.73893 | 0.73129 | 0.69986 |
| Score Diff <= 2 | 0.94799 | 0.95033 | 0.94555 | 0.93502 |

## Improvements and Some Notes
 - Increasing the features will marginally increase the accuracy
 - More data (Some of the anime only have a few hundred ratings)
 - Guessing the median score yields an accuracy of about 30% so a linear regression works substantially better.
 - The more anime the user has watched, the more accurate the predictor is
 - Fuzzy k-means and k-means can be used to cluster anime and find groups

## Conclusion
A linear regression recommender system generally works pretty well. With a regularization parameter of 15 and 1000 features, 
it can get 45% of all scores correct, 75% of all scores correct within one point, and 95% of all scores correct within two points.
However, it might not be the case that anime preferences can be linearly separable, so non-linear methods might be needed for further
accuracy (maybe SVMs or self organizing maps?).
