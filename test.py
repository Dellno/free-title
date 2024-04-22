from flask import Flask, render_template
from forms.register_form import RegisterForm
from forms.login import LoginForm
import datetime
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from forms.Game_form import GameForm
from data.game import Game

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(
    days=1)
login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='free-title', projects=[[[], [], [], []]])


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')




