from flask.ext.wtf import Form
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired

class SearchForm(Form):
    query = StringField('query', validators=[DataRequired()])
    count = IntegerField('count', default=5)