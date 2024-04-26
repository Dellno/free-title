from flask import Flask, render_template, redirect, session, make_response, request, jsonify
from data import db_session
from data.user import User
from forms.register_form import RegisterForm
from forms.login import LoginForm
import datetime
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from forms.Game_form import GameForm
from data.game import Game
import freeTitle_api
from get_game import get_game
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(
    days=1)
login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/')
@app.route('/index', methods=['POST'])
def index():
    return render_template('index.html', title='free-title', projects=get_game())


@app.route('/submit/<game_id>', methods=['POST'])  # эта функция вызывается при нажатии кнопки
def submit_form(game_id=None):
    if not current_user.is_authenticated:
        return redirect("/login")
    db_sess = db_session.create_session()
    game = db_sess.query(Game).filter(Game.id == game_id).first()
    if str(current_user.id) not in str(game.liked_user).split("_"):
        game.raiting += 1
        game.liked_user += f"_{str(current_user.id)}"
    else:
        game.raiting -= 1
        us = f"_{current_user.id}"
        sp = game.liked_user.index(us)
        game.liked_user = game.liked_user[:sp] + game.liked_user[sp + len(us):]
    db_sess.commit()
    return redirect('/')


@app.route('/my_project')
def my_project():
    if not current_user.is_authenticated:
        return redirect("/login")
    return render_template('my_project.html', title='free-title', projects=get_game(author_id=current_user.id))


@app.route('/profile/<autor_id>')
def profile(autor_id=None):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == autor_id).first()
    games = get_game(author_id=autor_id)
    raiting = 0
    for i in games:
        raiting += i[2]

    if not current_user.is_authenticated:
        return redirect("/login")
    if current_user.id == int(autor_id):
        return render_template('my_profile.html', title='free-title', name=user.name, raiting=raiting,
                               projects=games, TG_token=f'api_token: {user.api_token}')
    else:
        return render_template('profile.html', title='free-title', name=user.name, raiting=raiting,
                               projects=games)


@app.route('/register', methods=['GET', 'POST'])
def register():
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


@app.route('/add_game', methods=['GET', 'POST'])
def add_game():
    if not current_user.is_authenticated:
        return redirect("/login")

    form = GameForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        game = Game()
        game.name = form.title.data
        game.content = form.content.data
        game.creator_id = current_user.id
        current_user.game.append(game)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('add_game.html', title='Добавить игру',
                           form=form)


@app.route("/project/<project_id>")
def project_title(project_id=None):
    if not project_id:
        print(project_id)
        return redirect("/")
    db_sess = db_session.create_session()
    game = db_sess.query(Game).filter(Game.id == project_id).first()
    if game:
        return render_template("project.html", title=f"проект {game.name}",
                               project_name=game.name,
                               name=f"Aвтор: {db_sess.query(User).filter(Game.creator_id == User.id).first().name}",
                               description=game.content, img=game.icon_path)


def main():
    db_session.global_init("db/game_and_user.db")
    app.register_blueprint(freeTitle_api.blueprint)
    app.run()


if __name__ == '__main__':
    main()
