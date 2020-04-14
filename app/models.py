from flask import current_app
from sqlalchemy.ext.hybrid import hybrid_property

from app import db
from app.solver import generate_valid_words
from app.utils import generate_uuid


class BoggleBoard(db.Model):
    __tablename__ = "boggle_boards"

    id = db.Column(db.String(6), primary_key=True)

    dice = db.Column(db.String(17))  # TODO: consider a more normalised form since "Qu" will not always be present

    def __init__(self, board):
        self.id = generate_uuid()
        self.dice = "".join(["".join(row) for row in board])

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

    @hybrid_property
    def all_words(self):
        return generate_valid_words(self.generate_board(), current_app.dictionary)
