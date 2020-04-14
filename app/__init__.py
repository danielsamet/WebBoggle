from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from app.config import Config

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db, Config.MIGRATIONS_DIR)

    from app.routes import bp
    app.register_blueprint(bp)

    with open("words_alpha_collins.txt", encoding="utf8") as file:
        words = file.read().split("\n")

    from app.solver import build_word_dictionary
    app.dictionary = build_word_dictionary(words)

    return app


if __name__ == '__main__':
    create_app().run()
