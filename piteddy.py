from TwitterAPI import TwitterAPI, TwitterOAuth
import pyvona
import os

def init_twitter_api():
  o = TwitterOAuth.read_file("credentials.txt") 
  api = TwitterAPI(o.consumer_key,
                 o.consumer_secret,
                 o.access_token_key,
                 o.access_token_secret)  

   
  return api

def init_ivona():
  creds = read_credentials('ivona_credentials.txt')
  v = pyvona.create_voice(creds['access_key'], creds['secret_key'])
  return v

def read_credentials(filename):
  if filename is None:
     path = os.path.dirname(__file__)
     filename = os.path.join(path, 'ivona_credentials.txt')
 
  with open(filename) as f:
    creds = {}
    for line in f:
      if '=' in line:
	name, value = line.split('=', 1)
    	creds[name.strip()] = value.strip()
    return creds	


def search_last_tweets(query, tweets_number): 
  for item in api.request('search/tweets', {'q': query, 'count': tweets_number}):
    #print(item['text'] if 'text' in item else item)    
    content = item['text']
    print(content)
    ivona.speak(content)	   

api = init_twitter_api()
ivona = init_ivona()
search_last_tweets('Donald Trump', 5)
