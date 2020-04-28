from flask import render_template, jsonify, redirect, url_for, Blueprint

from app import db
from app.models import BoggleBoard

bp = Blueprint("routes", __name__)


@bp.app_errorhandler(404)
def not_found_error():
    return redirect(url_for("routes.index"))


@bp.route('/')
def index():
    return render_template("index.html")


@bp.route("/generate_board", methods=["POST"])
def generate_board():
    boggle_board = BoggleBoard()

    db.session.add(boggle_board)
    db.session.commit()

    return jsonify({"game_id": boggle_board.id, "board": boggle_board.generate_board(),
                    "words": sorted(boggle_board.generate_words())}), 200


@bp.route('/join/<game_id>')
def boggle_board(game_id):
    board = BoggleBoard.query.filter_by(id=game_id).first()

    if not board:
        return redirect(url_for("routes.index"))

    return render_template("index.html", game_id=board.id, dice=board.generate_board(),
                           words=sorted(board.generate_words()))
