from flask import Flask, render_template, redirect, session, make_response, request
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


def get_game(count=20, start=1, author_id=None):
    last_id = start
    popular_project = []
    db_sess = db_session.create_session()
    for i in range(count):

        if not author_id:
            game = db_sess.query(Game).filter(last_id <= Game.id).first()
            if game:
                author = db_sess.query(User).filter(game.creator_id == User.id).first()
        else:
            game = db_sess.query(Game).filter(last_id <= Game.id).filter(Game.creator_id == author_id).first()
            if game:
                author = db_sess.query(User).filter(User.id == author_id).first()
        last_id += 1
        if not game is None:
            if len(game.content) > 80:
                popular_project.append([
                    game.name, author.name, game.raiting, game.content[:79] + "...", game.id, game.creator_id
                ])
            else:
                popular_project.append([
                    game.name, author.name, game.raiting, game.content, game.id, game.creator_id
                ])

    return popular_project


@app.route('/')
@app.route('/index', methods=['POST'])
def index():
    return render_template('index.html', title='free-title', projects=get_game())


@app.route('/submit', methods=['POST']) # эта функция вызывается при нажатии кнопки
def submit_form():
    print(1) # сюда пиши че хочешь
    return redirect('/')


@app.route('/my_project')
@login_required
def my_project():
    return render_template('my_project.html', title='free-title', projects=get_game(author_id=current_user.id))


@app.route('/profile/<autor_id>')
@login_required
def profile(autor_id):
    return render_template('profile.html', title='free-title', name=get_game(author_id=autor_id)[0][1], raiting=0,
                           projects=get_game(author_id=autor_id), TG_token='telegram_token')


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
@login_required
def add_game():
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
                               name=db_sess.query(User).filter(Game.creator_id == User.id).first().name,
                               description=game.content, img='')


def main():
    db_session.global_init("db/game_and_user.db")
    app.run()


if __name__ == '__main__':
    main()
