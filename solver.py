import random
import time

from app import BoggleBoard
from config import Config


def generate_valid_words(board):
    valid_words = []

    # TODO: fill in algorithm here

    return valid_words


if __name__ == '__main__':
    board_dice = random.sample(Config.DICE, len(Config.DICE))
    board = []

    for _ in range(4):
        board.append([random.choice(board_dice.pop()) for __ in range(4)])

    boggle_board = BoggleBoard(board)

    start = time.time()
    word_list = generate_valid_words(boggle_board.board)

    end = time.time()

    print(f"{len(word_list)} words were generated in {end - start:.6f} seconds")
