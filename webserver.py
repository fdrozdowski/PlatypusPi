from flask import Flask, render_template, redirect
from forms import SearchForm
from piteddy import *



app = Flask(__name__)
app.config.from_object('config')
api = init_twitter_api()
ivona = init_ivona()


@app.route('/', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    if form.validate_on_submit():
      query = form.query.data
      count = form.count.data
      print('Search for="%s", #times=%s' % (query, str(count)))
      search_last_tweets(query, count)
      return redirect('/')
      
    return render_template('index.html', 
                           title='Search Tweets',
                           form=form)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')