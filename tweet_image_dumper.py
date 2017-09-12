#!/usr/bin/env python
# encoding: utf-8

from twitter_credentials import *
import tweepy #https://github.com/tweepy/tweepy
import csv
import sys

first_tweet_id = 870179852644700160 # from June 1st 2017
first_tweet_id = 907684109497126912 # from September 12th 2017

def get_all_tweets(screen_name):
    #Twitter only allows access to a users most recent 3240 tweets with this method

    #authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    #initialize a list to hold all the tweepy Tweets
    alltweets = []

    #make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name = screen_name,count=1)

    #save most recent tweets
    alltweets.extend(new_tweets)

    #save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1

    #keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        print ("getting tweets before %s" % (oldest))

        #all subsequent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest, since_id=first_tweet_id)

        #save most recent tweets
        alltweets.extend(new_tweets)

        #update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

        print ("...%s tweets downloaded so far" % (len(alltweets)))

    #go through all found tweets and remove the ones with no images 
    outtweets = [] #initialize master list to hold our ready tweets
    for tweet in alltweets:
        #not all tweets will have media url, so lets skip them
        try:
            print (tweet.entities['media'][0]['media_url'])
        except (NameError, KeyError):
            media_url = ''
        else:
            #got media_url - means add it to the output
            media_url = tweet.entities['media'][0]['media_url']
        outtweets.append([tweet.id_str, tweet.created_at, tweet.text.replace("\n",'\\n'), media_url])

    #write the csv  
    with open('%s_tweets.csv' % screen_name, 'w') as f:
        writer = csv.writer(f, dialect=csv.get_dialect("unix"))
        writer.writerow(["id","created_at","text","media_url"])
        writer.writerows(outtweets)


if __name__ == '__main__':
    #pass in the username of the account you want to download
    get_all_tweets("RTWbike")
