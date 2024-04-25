from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileRequired


class GameForm(FlaskForm):
    title = StringField('Название игры', validators=[DataRequired()])
    content = TextAreaField("Описание")
    submit = SubmitField('Создать')
    icon = FileField("перетащите сюда изображение", validators=[FileRequired()])
