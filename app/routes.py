import random

from flask import render_template, jsonify, redirect, url_for, Blueprint

from app import db
from app.models import BoggleBoard
from app.config import Config


bp = Blueprint("routes", __name__)


@bp.route('/')
def index():
    return render_template("index.html")


@bp.route("/generate_board", methods=["POST"])
def generate_board():
    board_dice = random.sample(Config.DICE, len(Config.DICE))
    board = []

    for _ in range(4):
        board.append([random.choice(board_dice.pop()) for __ in range(4)])

    boggle_board = BoggleBoard(board)

    db.session.add(boggle_board)
    db.session.commit()

    return jsonify({"game_id": boggle_board.id, "board": board, "words": sorted(boggle_board.generate_words())}), 200


@bp.route('/join/<game_id>')
def boggle_board(game_id):
    board = BoggleBoard.query.filter_by(id=game_id).first()

    if not board:
        return redirect(url_for("index"))

    return render_template("index.html", game_id=board.id, dice=board.generate_board(), words=sorted(board.generate_words()))
