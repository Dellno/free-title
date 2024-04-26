from flask import Blueprint, jsonify, make_response
from data import db_session
from data.game import Game
from data.user import User
from get_game import get_licked_game
import json


blueprint = Blueprint(
    'free-title_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/<token>')
def get_licked(token=None):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.api_token == token).first()
    if token is None:
        return make_response(jsonify({'error': 'Not found'}), 404)

    if user is None:
        return make_response(jsonify({'error': 'Bad Request'}), 400)

    resp = []
    gc = 0
    for game in get_licked_game(user.id):
        resp.append( {"name":
            game.name, "content": game.content, "author":db_sess.query(User).filter(game.creator_id == User.id).first().name
        }        )
        gc += 1
    print(resp)
    return jsonify(json.dumps(resp))
