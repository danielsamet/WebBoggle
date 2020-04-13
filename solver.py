import random
import time

from app import BoggleBoard
from config import Config


def generate_valid_words(board, dictionary_words):
    valid_words = []

    # TODO: fill in algorithm here

    return valid_words


if __name__ == '__main__':
    def generate_board(dice=None):
        if not dice:
            board_dice = random.sample(Config.DICE, len(Config.DICE))

            board = []
            for _ in range(4):
                board.append([random.choice(board_dice.pop()) for __ in range(4)])

        else:
            board = [[dice[i + j] for j in range(4)] for i in range(4)]

        return BoggleBoard(board)


    def run_generator(board):
        start = time.time()
        word_list = generate_valid_words(generate_board().board, words)
        end = time.time()

        print(f"{len(word_list)} words were generated in {end - start:.6f} seconds")


    with open("words_alpha.txt") as file:
        words = file.read().split("\n")

    print("\nPreconfigured board:")
    print("-" * 20)
    run_generator(generate_board("LOPGPOCIHBIEGKLS"))

    print("\nRandom board:")
    print("-" * 20)
    run_generator(generate_board())
