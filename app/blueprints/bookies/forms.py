from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class SearchInput(FlaskForm):
    search_str = StringField('Title or author: ', validators=[DataRequired()])
    submit_btn = SubmitField('Find')

class ChatInput(FlaskForm):
    chat_input = StringField('', validators=[DataRequired()])