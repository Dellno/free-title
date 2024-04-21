from flask import Flask, render_template, redirect, session, make_response
from data import db_session
from data.user import User
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
    return render_template('index.html', title='free-title', projects=[])


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.login == form.login.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            login=form.login.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.login == form.login.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('sing_in.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('sing_in.html', title='Авторизация', form=form)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/add_game',  methods=['GET', 'POST'])
@login_required
def add_news():
    form = GameForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        game = Game()
        game.title = form.title.data
        game.content = form.content.data
        current_user.game.append(game)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('add_game.html', title='Добавить игру',
                           form=form)


def main():
    db_session.global_init("db/game_and_user.db")
    app.run()


if __name__ == '__main__':
    main()
