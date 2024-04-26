from data import db_session
from data.user import User
from data.game import Game


def get_game(author_id=None):
    popular_project = []
    db_sess = db_session.create_session()
    if not author_id:
        games = db_sess.query(Game).all()
    else:
        games = db_sess.query(Game).filter(Game.creator_id == author_id).all()
    if games:
        for game in games:
            author = db_sess.query(User).filter(game.creator_id == User.id).first()
            if len(game.content) > 80:
                popular_project.append([
                    game.name, author.name, game.raiting, game.content[:79] + "...", game.id, game.creator_id
                ])
            else:
                popular_project.append([
                    game.name, author.name, game.raiting, game.content, game.id, game.creator_id
                ])
    popular_project = list(sorted(popular_project, key=lambda x: x[2])) 
    return popular_project


def get_licked_game(user_id):
    licked_game = []
    db_sess = db_session.create_session()
    games = db_sess.query(Game).all()
    for game in games:
        if str(user_id) in str(game.liked_user).split("_"):
            licked_game.append(game)
    return licked_game
