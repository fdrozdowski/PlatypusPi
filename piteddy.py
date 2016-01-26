from TwitterAPI import TwitterAPI, TwitterOAuth
import pyvona
import os
import nytimes
import time


class PiTeddy:
  def __init__(self):
    self.api = self.init_twitter_api()
    self.ivona = self.init_ivona()
    self.nyt = self.init_nyt()

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
    voice.voice_name = 'Brian'
    voice.speech_rate = 'slow'
    return voice

  def init_nyt(self):
    creds = self.read_credentials('nyt_credentials.txt')
    search_api = nytimes.get_article_search_obj(creds['article_search_api_key'])
    return search_api

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

  def play_tweets(self, query, count):
    for item in self.api.request('search/tweets', {'q': query, 'count': count}):
      #print(item['text'] if 'text' in item else item)
      words = item['text']
      # remove urls from content
      content = ' '.join(word for word in words.split() if not 'http' in word)
      print(content)
      self.ivona.speak(content)

  def play_news(self, count, query):

    if query == None:
      articles = self.nyt.article_search(begin_date = time.strftime("%Y%m%d"))
    else:
      articles = self.nyt.article_search(q = query)

    counter = 0
    for article in articles['response']['docs']:
      print "snippet: " + article['snippet']
      self.ivona.speak(article['snippet'])
      counter += 1
      if counter == count:
        break
