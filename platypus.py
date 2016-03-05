from TwitterAPI import TwitterAPI, TwitterOAuth
import pyvona
import os
import nytimes
import time
import requests



class PlatypusPi:
  def __init__(self):
    self.api = self.init_twitter_api()
    self.ivona = self.init_ivona()
    self.nyt_articles = self.init_nyt_articles()
    self.nyt_topstories_key = self.init_nyt_topstories()
    self.nyt_sections = ["home", "world", "national", "politics", "nyregion",
      "business", "opinion", "technology", "science", "health", "sports",
      "arts", "fashion", "dining", "travel", "magazine", "realestate"]

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
    return voice

  def init_nyt_articles(self):
    creds = self.read_credentials('nyt_credentials.txt')
    search_api = nytimes.get_article_search_obj(creds['article_search_api_key'])
    return search_api

  def init_nyt_topstories(self):
    creds = self.read_credentials('nyt_credentials.txt')
    stories_api_key = creds['top_stories_api_key']
    return stories_api_key  

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

  def change_voice(self, name):
    if name in ['Brian', 'Amy', 'Emma', 'Raveena', 'Gwyneth', 'Geraint',
     'Nicole', 'Russell', 'Justin', 'Salli', 'Joey', 'Kimberly', 'Kendra',
     'Eric', 'Jennifer', 'Ivy', 'Chipmunk']:
      self.ivona.voice_name = name  
    else:
      self.ivona.speak("Incorrect Ivona name provided.")  

  def change_speech_rate(self, rate):
    if rate in ['x-slow', 'slow', 'medium', 'fast', 'x-fast']:
      self.ivona.speech_rate = rate
    else:
      self.ivona.speak("Incorrect Ivona speech rate provided.")

  def focus(self):
    self.ivona.speak("Loyce!!! Focus!!!");

  def play_tweets(self, query, count):

    if count < 1:
      count = 1

    for item in self.api.request('search/tweets', {'q': query, 'count': count}):
      words = item['text']
      # remove urls from content
      content = ' '.join(word for word in words.split() if not 'http' in word)
      print(content)
      self.ivona.speak(content)

  def play_nyt_articles(self, query, count):

    if count < 1:
      count = 1

    if len(query) == 0:
      articles = self.nyt_articles.article_search(begin_date = time.strftime("%Y%m%d"))
    else:
      articles = self.nyt_articles.article_search(q = query)

    counter = 0
    for article in articles['response']['docs']:

      print "snippet: " + article['snippet']
      self.ivona.speak(article['snippet'])
      counter += 1
      if counter == count:
        break

  def play_nyt_topstories(self, section, count):

    if count < 1:
      count = 1

    if section not in self.nyt_sections:
      self.ivona.speak('Incorrect New York Times section name provided.')
      return 'Incorrect section name'

    articles = r = requests.get('http://api.nytimes.com/svc/topstories/v1/' + 
      section + '.json?api-key=' + self.nyt_topstories_key)

    articles_list = articles.json()['results']

    if len(articles_list) == 0:
      self.ivona.speak('No articles found in this section.')
      return 'No articles found in this section'

    counter = 0
    for article in articles_list:
     
      title = article['title']
      abstract = article['abstract']

      print "title: " + article['title'] + "\nabstract: " + article['abstract']

      if title:
        self.ivona.speak('Title: ' + title)
      else:
        self.ivona.speak('No title provided.')

      if abstract:
        self.ivona.speak('Abstract: ' + abstract)
      else:
        self.ivona.speak('No abstract provided.')
      counter += 1
      if counter == count:
        break