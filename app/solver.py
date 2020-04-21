import time

from app import create_app


def generate_valid_words(board, dictionary_words, min_word_size=3):
    def get_words(coordinates, word_dictionary, traversed_nodes=None):
        """returns all words attainable from a specified coordinate"""

        if not traversed_nodes:
            traversed_nodes = [coordinates]

        curr_letter = board[coordinates[0]][coordinates[1]]

        if curr_letter == "QU":
            new_word_dictionary = word_dictionary[1]["Q"][1]["U"]
        else:
            new_word_dictionary = word_dictionary[1][curr_letter]

        if new_word_dictionary[0]:
            if len(new_word_dictionary[0]) >= min_word_size and new_word_dictionary[0] not in valid_words:
                valid_words.append(new_word_dictionary[0])

        for surrounding_node in set(surrounding_nodes_map[coordinates]) - set(traversed_nodes):
            next_letter = board[surrounding_node[0]][surrounding_node[1]]
            next_letter = next_letter if next_letter != "QU" else "Q"

            if next_letter in new_word_dictionary[1]:
                try:
                    get_words(surrounding_node, new_word_dictionary, traversed_nodes + [surrounding_node])
                except KeyError:
                    continue

    valid_words = []
    surrounding_nodes_map = _generate_surrounding_nodes(4)

    for row_index in range(len(board)):
        for col_index in range(len(board[row_index])):
            get_words((row_index, col_index), dictionary_words)

    return valid_words


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


def _get_surrounding_nodes(coordinates):
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


def _generate_surrounding_nodes(board_size=4):
    """generates a dictionary of precomputed surrounding nodes"""

    surrounding_nodes = {}

    for row in range(board_size):
        for column in range(board_size):
            surrounding_nodes[row, column] = _get_surrounding_nodes((row, column))

    return surrounding_nodes


if __name__ == '__main__':  # TEST CODE
    from app.models import BoggleBoard


    def run_generator(board):
        start = time.time()
        # board.pretty_print()
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
        run_generator(BoggleBoard("EDRQuHIECTSAZNLSE"))

        print("\nRandom board:")
        print("-" * 20)
        run_generator(BoggleBoard())
