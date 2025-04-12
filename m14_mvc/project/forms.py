# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired

class BookForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired()])
    author = StringField('Author', validators=[InputRequired()])