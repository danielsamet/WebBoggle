import random

from flask import Flask, render_template, jsonify, redirect, url_for
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property

from config import Config
from utils import generate_uuid

application = Flask(__name__)
application.config.from_object(Config)

db = SQLAlchemy(application)
migrate = Migrate(application, db, Config.MIGRATIONS_DIR)


class BoggleBoard(db.Model):
    __tablename__ = "boggle_boards"

    id = db.Column(db.String(6), primary_key=True)

    dice = db.Column(db.String(17))  # TODO: consider a more normalised form since "Qu" will not always be present

    def __init__(self, board):
        self.id = generate_uuid()
        self.dice = "".join(["".join(row) for row in board])

    @hybrid_property
    def board(self):
        """returns a 2 dimensional array for the dice"""

        table = []
        q_offset = 0

        for i in range(4):
            row = []
            for col in range(4):
                die = self.dice[i * 4 + col + q_offset]
                if die == "Q":
                    die = "Qu"
                    q_offset += 1
                row.append(die)
            table.append(row)

        return table


@application.route('/')
def index():
    return render_template("index.html")


@application.route("/generate_board", methods=["POST"])
def generate_board():
    board_dice = random.sample(Config.DICE, len(Config.DICE))
    board = []

    for _ in range(4):
        board.append([random.choice(board_dice.pop()) for __ in range(4)])

    boggle_board = BoggleBoard(board)

    db.session.add(boggle_board)
    db.session.commit()

    return jsonify({"game_id": boggle_board.id, "board": board}), 200


@application.route('/join/<game_id>')
def boggle_board(game_id):
    board = BoggleBoard.query.filter_by(id=game_id).first()

    if not board:
        return redirect(url_for("index"))

    return render_template("index.html", game_id=board.id, dice=board.board)


if __name__ == '__main__':
    application.run()
