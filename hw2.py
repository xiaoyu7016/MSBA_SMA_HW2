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

raw_tweets = crawl_tweets("zika",100)
messaged_tweets = one_tweet_per_element(raw_tweets)
## Why list elements < 100 * 100??

####################################
# formatting to nice csv-ish file
####################################
def collect_tweet_level_field_from_each_user(title_string,messaged_tweets_list):
    """Retrieve info at per-tweet level"""
    empty_list = []
    for i in range(len(messaged_tweets_list)):
        empty_list.append(messaged_tweets_list[i][title_string])
    
    return empty_list
    
def collect_user_level_field_from_each_user(title_string,messaged_tweets_list):
    """Retrieve info at per-user level"""    
    empty_list = []
    for i in range(len(messaged_tweets_list)):
        empty_list.append(messaged_tweets_list[i]['user'][title_string])
    
    return empty_list

# Tweet level fields
messaged_tweets[0].keys()

tweet_id = collect_tweet_level_field_from_each_user('id',messaged_tweets)
text = collect_tweet_level_field_from_each_user('text',messaged_tweets)
retweet_count = collect_tweet_level_field_from_each_user('retweet_count',messaged_tweets)

# Second layer fields
messaged_tweets[0]['user'].keys()

user_id = collect_user_level_field_from_each_user('id',messaged_tweets)
following = collect_user_level_field_from_each_user('following',messaged_tweets)
followers_count = collect_user_level_field_from_each_user('followers_count',messaged_tweets)
listed_count = collect_user_level_field_from_each_user('listed_count', messaged_tweets)
friends_count = collect_user_level_field_from_each_user('friends_count',messaged_tweets)
favourites_count =   collect_user_level_field_from_each_user('favourites_count',messaged_tweets)
statuses_count = collect_user_level_field_from_each_user('statuses_count', messaged_tweets)
location = collect_user_level_field_from_each_user('location',messaged_tweets)
created_at = collect_user_level_field_from_each_user('created_at',messaged_tweets)
verified = collect_user_level_field_from_each_user('verified',messaged_tweets)
description = collect_user_level_field_from_each_user('description',messaged_tweets)

tweets_dict = {
    'tweet_id' : tweet_id,
    'text' : text,
    'retweet_count' : retweet_count,
    'user_id' : user_id,
    'following' : following,
    'followers_count' : followers_count,
    'listed_count' : listed_count,
    'friends_count' : friends_count,
    'favourites_count' : favourites_count,
    'statuses_count' : statuses_count,
    'location' : location,
    'created_at' : created_at,
    'verified' : verified,
    'description' :description
    
}

tweets_df = pd.DataFrame(data = tweets_dict, columns = tweets_dict.keys())

tweets_df.to_csv('zika_tweets_per_tweet.csv', encoding = 'utf-8')