# -*- coding: utf-8 -*-
"""
Created on Sat Jan 30 15:33:13 2016
Task 1

@author: Yuwen Wang
"""
import os
from pandas import DataFrame,Series
import pandas as pd

zika = pd.read_csv('zika_tweets_per_tweet.csv')

taska = zika[['user_id','listed_count','retweet_count','followers_count','following']]
taska.describe()

retweet_by_user = pd.DataFrame(taska.groupby('user_id')['retweet_count'].sum())
user_info = taska.groupby('user_id')[['listed_count','followers_count','following']].mean()

taska_by_user = pd.merge(user_info,retweet_by_user,left_index = True, right_index = True)

# Log-transform all features
def log_trans(x):
    return np.log(x+1)  # +1 to take care of 0 values

for column in taska_by_user:
    taska_by_user[column] = log_trans(taska_by_user[column])

# Coefficients learnt:
follower = 0.10919318
following = -0.00270281
listed = 0.2451884
retweet = 0.04542407

# Rescale s.t. sum up to 1
scaler = 1/(follower+following+listed+retweet)
follower *= scaler
following *= scaler
listed *= scaler
retweet *= scaler

taska_by_user['influence_score'] = taska_by_user['listed_count'] * listed + taska_by_user['followers_count'] * follower + taska_by_user['following'] * following + taska_by_user['retweet_count'] * retweet

# Rank by influence_score and get TOP 50
Influencer_top50 = taska_by_user.sort(columns = 'influence_score', ascending = False)[:50]


############################
"""
Questions:
1. The coefficients are learnt on log(diff), can we directly apply that in the absolute case?
2. Why do we have to normalize features, given that coefficients are learnt from non-normalized features? 