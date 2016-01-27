# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 22:10:41 2016

@author: Yuwen Wang
"""
from twython import Twython
import csv

from pandas import DataFrame, Series
import pandas as pd


####################
# Authorization
####################
APP_KEY = "2lzEpNDwz9ieHhr738sXX8Avl"
APP_SECRET = "z3srlvggHvhCqIBSMnKRbn5OY36B2Z58299ipfKtuRXMqwI4rj"

twitter_get_token = Twython(APP_KEY,APP_SECRET,oauth_version=2)
ACCESS_TOKEN = twitter_get_token.obtain_access_token()

twitter = Twython(APP_KEY,access_token = ACCESS_TOKEN)


def crawl_tweets(topic_string,num_of_calls):
    """A function to crawl tweets
       (1) query topic is specified by "topic_string"
       (2) num_of_calls has an upper limit of 450 per access token which is valid for 15 min;
           each call will crawl 100 tweets
       (3) returns a list, each element contains 100 tweets"""
    empty_list = []
    for i in range(num_of_calls):
        empty_list.append(twitter.search(q=topic_string,count=100))
    
    return empty_list

def one_tweet_per_element(raw_tweets_list):
    empty_list = []
    for i in range(len(raw_tweets_list)):
        empty_list += raw_tweets_list[i]['statuses']
        
    return empty_list

raw_tweets = crawl_tweets("food",100)
messaged_tweets = one_tweet_per_element(raw_tweets)
## Why list elements < 100 * 100??

####################################
# formatting to nice csv-ish file
####################################

def collect_1st_layer_field_from_each_user(title_string,messaged_tweets_list):

    """ NOT WORKING"""
    
    empty_list = []
    for i in range(len(messaged_tweets_list)):
        empty_list.append(messaged_tweets_list[title_string])
    
    return empty_list

text = collect_1st_layer_field_from_each_user('text',messaged_tweets)


with open('mycsvfile.csv', 'wb') as f:  # Just use 'w' mode in 3.x
    w = csv.DictWriter(f, my_dict.keys())
    w.writeheader()
    w.writerow(my_dict)