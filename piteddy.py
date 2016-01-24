from TwitterAPI import TwitterAPI, TwitterOAuth
from espeak import espeak
import codecs
import os

def init_twitter_api():
  o = TwitterOAuth.read_file("credentials.txt") 
  api = TwitterAPI(o.consumer_key,
                 o.consumer_secret,
                 o.access_token_key,
                 o.access_token_secret)  

  return api


def search_last_tweets(query, tweets_number): 
  for item in api.request('search/tweets', {'q': query, 'count': tweets_number}):
    #print(item['text'] if 'text' in item else item)    
    content = item['text']
    content = content.encode('ascii', 'ignore')
    #content = content.replace('...', 'dot dot dot')
    print(content)	   
    espeak.synth(content)

api = init_twitter_api()
search_last_tweets('Donald Trump', 5)
