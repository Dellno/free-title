from flask import Flask, render_template


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/')
@app.route('/index/<t>')
def index(t=''):
    return render_template('index.html', title=t)


def main():
    app.run()


if __name__ == '__main__':
    main()