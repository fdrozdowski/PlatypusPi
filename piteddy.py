from TwitterAPI import TwitterAPI, TwitterOAuth
import pyvona
import os


class PiTeddy:
  def __init__(self):
    self.api = self.init_twitter_api()
    self.ivona = self.init_ivona()
    
  def init_twitter_api(self):
    o = TwitterOAuth.read_file("credentials.txt") 
    api = TwitterAPI(o.consumer_key,
                   o.consumer_secret,
                   o.access_token_key,
                   o.access_token_secret)  
    return api

  def init_ivona(self):
    creds = self.read_credentials('ivona_credentials.txt')
    voice = pyvona.create_voice(creds['access_key'], creds['secret_key'])
    voice.voice_name = 'Ivy'
    voice.speech_rate = 'slow'
    return voice

  def read_credentials(self, filename):
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

  def play_tweets(self, query, tweets_number): 
    for item in self.api.request('search/tweets', {'q': query, 'count': tweets_number}):
      #print(item['text'] if 'text' in item else item)    
      words = item['text']
      content = ' '.join(word for word in words.split() if not 'http' in word) # remove urls from content
      print(content)
      self.ivona.speak(content)	   

