from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from app.config import Config

db = SQLAlchemy()
migrate = Migrate()


def create_app(config_object=Config):
    app = Flask(__name__)
    app.config.from_object(config_object)

    db.init_app(app)
    migrate.init_app(app, db, config_object.MIGRATIONS_DIR)

    from app.routes import bp
    app.register_blueprint(bp)

    with open(config_object.DICTIONARY_ADDRESS, encoding="utf8") as file:
        words = file.read().split("\n")

    from app.solver import build_word_dictionary
    app.dictionary = build_word_dictionary(words, config_object.MIN_WORD_SIZE)

    @app.shell_context_processor  # adds automatic context to the shell
    def make_shell_context():
        from app.models import BoggleBoard, WordCount

        return dict(app=app, db=db, BoggleBoard=BoggleBoard, WordCount=WordCount)

    return app


if __name__ == '__main__':
    create_app().run()
