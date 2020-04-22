from app import create_app, Config, db
from app.models import BoggleBoard, WordCount


def generate_boards(num_board=1000):
    """generates and solves boards num_board times"""

    for _ in range(num_board):
        db.session.add(BoggleBoard(calculate_all_words=True))
        db.session.commit()


def get_board_stats(min_word_size="all"):
    stats = {}

    word_sizes = [3, 4, 5] if min_word_size == "all" else min_word_size

    for word_size in word_sizes:
        stats[word_size] = {}

        word_counts = [count.num_words for count in WordCount.query.filter_by(min_word_size=word_size).all()]

        stats[word_size]["ttl"] = len(word_counts)
        stats[word_size]["min"] = min(word_counts)
        stats[word_size]["max"] = max(word_counts)
        stats[word_size]["avg"] = f"{sum(word_counts) / stats[word_size]['ttl']:.2f}"

    return stats


if __name__ == '__main__':
    with create_app(Config).app_context():
        for _ in range(100):
            generate_boards(100)
            print(get_board_stats())
