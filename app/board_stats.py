from app import create_app, Config, db
from app.models import BoggleBoard, WordCount


def generate_boards(num_board=1000):
    """generates and solves boards num_board times"""

    for _ in range(num_board):
        db.session.add(BoggleBoard(calculate_all_words=True))
        db.session.commit()


def print_board_stats():
    stats = {}

    word_sizes = list(range(3, 18))
    board_count = BoggleBoard.query.count()

    for word_size in word_sizes:
        stats[word_size] = {}

        word_counts = [count.num_words for count in WordCount.query.filter_by(word_size=word_size).all()]

        stats[word_size]["ttl"] = len(word_counts)  # occurrences of the word size across boards
        stats[word_size]["min"] = min(word_counts) if word_counts else 0  # least occurrences of the word size
        stats[word_size]["max"] = max(word_counts) if word_counts else 0  # most occurrences of the word size
        stats[word_size]["avg"] = f"{sum(word_counts) / board_count:.6f}" if word_counts else 0  # avg occ

        print(f"{word_size} - {stats[word_size]}")


if __name__ == '__main__':
    with create_app(Config).app_context():
        for _ in range(100):
            generate_boards(100)
            print_board_stats()
