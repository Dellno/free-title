from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired


class GameForm(FlaskForm):
    title = StringField('Название игры', validators=[DataRequired()])
    content = TextAreaField("Описание")
    submit = SubmitField('Создать')
