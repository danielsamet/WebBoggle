import random

from flask import current_app

from app import db
from app.solver import generate_valid_words
from app.utils import generate_uuid


class BoggleBoard(db.Model):
    __tablename__ = "boggle_boards"

    id = db.Column(db.String(6), primary_key=True)

    dice = db.Column(db.String(17))  # TODO: consider a more normalised form since "Qu" will not always be present

    # numbers below are used for identifying difficulty of boards
    valid_3_words = db.Column(db.Integer)  # stores number of valid 3 letter words attainable through the above dice
    valid_4_words = db.Column(db.Integer)  # stores number of valid 4 letter words attainable through the above dice
    valid_5_words = db.Column(db.Integer)  # stores number of valid 5 letter words attainable through the above dice

    def __init__(self, dice=None, calculate_all_words=False):
        self.id = generate_uuid()

        if not dice:
            dice = "".join(random.choice(die) for die in
                           random.sample(current_app.config["DICE"], len(current_app.config["DICE"])))

        self.dice = dice

        if calculate_all_words:
            self.valid_3_words = len(self.generate_words(3))
            self.valid_4_words = len(self.generate_words(4))
            self.valid_5_words = len(self.generate_words(5))

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
        return generate_valid_words(self.generate_board(), current_app.dictionary, min_word_size=min_word_size)


class WordCounts(db.Model):
    __tablename__ = "board_word_counts"

    id = db.Column(db.String(6), primary_key=True)

    min_word_size = db.Column(db.Integer)
