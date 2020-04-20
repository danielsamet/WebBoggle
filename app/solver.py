import time

from app import create_app


def generate_valid_words(board, dictionary_words, min_word_size=3):
    def get_surrounding_nodes(coordinates):
        nodes = []

        if coordinates[0] > 0:
            if coordinates[1] > 0:
                nodes.append((coordinates[0] - 1, coordinates[1] - 1))  # top left
            nodes.append((coordinates[0] - 1, coordinates[1]))  # top middle
            if coordinates[1] < 3:
                nodes.append((coordinates[0] - 1, coordinates[1] + 1))  # top right

        if coordinates[1] > 0:
            nodes.append((coordinates[0], coordinates[1] - 1))  # left
        if coordinates[1] < 3:
            nodes.append((coordinates[0], coordinates[1] + 1))  # right

        if coordinates[0] < 3:
            if coordinates[1] > 0:
                nodes.append((coordinates[0] + 1, coordinates[1] - 1))  # top left
            nodes.append((coordinates[0] + 1, coordinates[1]))  # top middle
            if coordinates[1] < 3:
                nodes.append((coordinates[0] + 1, coordinates[1] + 1))  # top right

        return nodes

    def get_words(coordinates, word_dictionary, traversed_nodes=None):
        """returns all words attainable from a specified coordinate"""

        if not traversed_nodes:
            traversed_nodes = [coordinates]

        words = []
        if word_dictionary[0]:
            if len(word_dictionary[0]) >= min_word_size:
                words = [word_dictionary[0]]

        for surrounding_node in set(get_surrounding_nodes(coordinates)) - set(traversed_nodes):
            if board[coordinates[0]][coordinates[1]] in word_dictionary[1]:
                words.extend(
                    get_words(
                        surrounding_node,
                        word_dictionary[1][board[coordinates[0]][coordinates[1]]],
                        traversed_nodes + [surrounding_node]
                    )
                )

        return set(words)

    valid_words = []

    for row_index in range(len(board)):
        for col_index in range(len(board[row_index])):
            valid_words.extend(get_words((row_index, col_index), dictionary_words))

    return list(set(valid_words))


def build_word_dictionary(word_list, min_word_size=3):
    def update_dictionary(dictionary, word):
        if word[0] not in dictionary[1]:
            dictionary[1][word[0]] = [False, {}]

        if len(word) == 1:
            dictionary[1][word[0]][0] = True
            return dictionary
        else:
            dictionary[1][word[0]] = update_dictionary(dictionary[1][word[0]], word[1:])
            return dictionary

    word_dictionary = [False, {}]

    for word in word_list:
        if len(word) < min_word_size:
            continue

        word = word.upper()

        word_dictionary = update_dictionary(word_dictionary, word)

        temp_dictionary = word_dictionary
        for letter in word:
            temp_dictionary = temp_dictionary[1][letter]
        temp_dictionary[0] = word

    return word_dictionary


if __name__ == '__main__':
    from app.models import BoggleBoard

    def run_generator(board):
        start = time.time()
        board.pretty_print()
        word_list = generate_valid_words(board.generate_board(uppercase_u=True), words)
        end = time.time()

        print(f"{len(word_list)} words were generated in {end - start:.6f} seconds")


    with open("words_alpha_collins.txt", encoding="utf8") as file:
        words = file.read().split("\n")

    start = time.time()
    words = build_word_dictionary(words)
    print(time.time() - start)

    with create_app().app_context():
        print("\nPreconfigured board:")
        print("-" * 20)
        run_generator(BoggleBoard("LOPGPOCIHBIEGKLS"))

        print("\nRandom board:")
        print("-" * 20)
        run_generator(BoggleBoard())
