import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI") or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MIGRATIONS_DIR = "migrations"

    DICE = [
        ['R', 'I', 'F', 'O', 'B', 'X'],
        ['I', 'F', 'E', 'H', 'E', 'Y'],
        ['D', 'E', 'N', 'O', 'W', 'S'],
        ['U', 'T', 'O', 'K', 'N', 'D'],
        ['H', 'M', 'S', 'R', 'A', 'O'],
        ['L', 'U', 'P', 'E', 'T', 'S'],
        ['A', 'C', 'I', 'T', 'O', 'A'],
        ['Y', 'L', 'G', 'K', 'U', 'E'],
        ['Qu', 'B', 'M', 'J', 'O', 'A'],
        ['E', 'H', 'I', 'S', 'P', 'N'],
        ['V', 'E', 'T', 'I', 'G', 'N'],
        ['B', 'A', 'L', 'I', 'Y', 'T'],
        ['E', 'Z', 'A', 'V', 'N', 'D'],
        ['R', 'A', 'L', 'E', 'S', 'C'],
        ['U', 'W', 'I', 'L', 'R', 'G'],
        ['P', 'A', 'C', 'E', 'M', 'D'],
    ]