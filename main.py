from flask import Flask, render_template
from data import db_session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='free-title')


def main():
    db_session.global_init("db/blogs.db")
    app.run()

    if __name__ == '__main__':
        main()
