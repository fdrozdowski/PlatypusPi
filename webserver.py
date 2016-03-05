from flask import Flask, render_template, redirect, request
from forms import SearchForm
from platypus import PlatypusPi
import json


app = Flask(__name__)
app.config.from_object('config')
platypus = PlatypusPi()


@app.route('/', methods=['GET', 'POST'])
def index():

  form = SearchForm(name='nam')
  if form.validate_on_submit():
    print request.form
    query = form.query.data
    count = form.count.data
    print('Search for="%s", #times=%s' % (query, str(count)))
    if 'nyt' in request.form:
      platypus.play_nyt_articles(query, count)
    if 'twitter' in request.form:
      platypus.play_tweets(query, count)
    return redirect('/')

  return render_template('index.html', 
                         title='Search Tweets',
                         form=form)

@app.route('/topstories', methods=['POST'])
def top_stories():
  
  json_data = request.data
  data_dict = json.loads(json_data)
  nytSection = data_dict['section']
  count = data_dict['count']
  print nytSection + " " + count
  platypus.play_nyt_topstories(nytSection, int(count))
  return "OK"

@app.route('/change_voice', methods=['POST'])
def change_voice():
  voice_name = request.data
  platypus.change_voice(voice_name)
  return "OK"

@app.route('/change_speech_rate', methods=['POST'])
def change_speech_rate():
  speech_rate = request.data
  platypus.change_speech_rate(speech_rate)
  return "OK"  

@app.route('/focus', methods=['GET'])
def focus_alarm():

  print "focus"
  platypus.focus()
  return "OK"  

@app.route('/weather', methods=['GET'])
def weather():
  platypus.play_current_weather()
  return "OK"  

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')