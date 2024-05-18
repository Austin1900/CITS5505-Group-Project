# forms.py
from wtforms import Form, StringField, SubmitField
from wtforms.validators import DataRequired


class SearchForm(Form):
    query = StringField('Search', validators=[DataRequired()])
    submit = SubmitField('Search')
