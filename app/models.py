import random

from flask import current_app

from app import db
from app.solver import generate_valid_words
from app.utils import generate_uuid


class BoggleBoard(db.Model):
    __tablename__ = "boggle_boards"

    id = db.Column(db.String(6), primary_key=True)

    dice = db.Column(db.String(17))  # TODO: consider a more normalised form since "Qu" will not always be present

    word_counts = db.relationship("WordCount", back_populates="board")

    def __init__(self, dice=None, calculate_all_words=False):
        self.id = generate_uuid()

        if not dice:
            dice = "".join(random.choice(die) for die in
                           random.sample(current_app.config["DICE"], len(current_app.config["DICE"])))

        self.dice = dice

        if calculate_all_words:
            self.word_counts.append(WordCount(3, len(self.generate_words(3))))
            self.word_counts.append(WordCount(4, len(self.generate_words(4))))
            self.word_counts.append(WordCount(5, len(self.generate_words(5))))

    def __repr__(self):
        return f"<BoggleBoard {self.id}>"

    def generate_board(self, uppercase_u=False):
        """returns a 2 dimensional array for the dice"""

        table = []
        q_offset = 0

        for i in range(4):
            row = []
            for col in range(4):
                die = self.dice[i * 4 + col + q_offset]
                if die == "Q":
                    die = "QU" if uppercase_u else "Qu"
                    q_offset += 1
                row.append(die)
            table.append(row)

        return table

    def pretty_print(self):
        for row in self.generate_board():
            print(row)

    def generate_words(self, min_word_size=3):
        return generate_valid_words(self.generate_board(uppercase_u=True), current_app.dictionary,
                                    min_word_size=min_word_size)


class WordCount(db.Model):
    __tablename__ = "board_word_counts"

    id = db.Column(db.Integer, primary_key=True)

    board_id = db.Column(db.Integer, db.ForeignKey("boggle_boards.id"))
    board = db.relationship("BoggleBoard", back_populates="word_counts")

    min_word_size = db.Column(db.Integer)
    num_words = db.Column(db.Integer)

    def __init__(self, min_word_size, num_words):
        self.min_word_size = min_word_size
        self.num_words = num_words

    def __repr__(self):
        return f"<Word Count {self.id} for BoggleBoard {self.board.id}>"
