# control all rendering of boards for both players and printing messages to the screen
# all validation is handled outside of the Display object, remember the
# interface

import itertools as it
import validator


class Display(object):

    VERTICAL_SHIP = '|'
    HORIZONTAL_SHIP = '-'
    EMPTY = 'O'
    MISS = '.'
    HIT = '*'
    SUNK = '#'

    """docstring for Display"""

    def __init__(self, board_size=10):
        self.BOARD_SIZE = board_size

    def prompt_for_names(self):

        self.clear_screen()

        players = []
        num = 1

        while len(players) < 2:

            confirm_name = 'n'

            while confirm_name != 'y':
                player_name = input("What is Player {}'s name? ".format(num))
                confirm_name = input(
                    "Thanks {}! That's what you want to be called right? [Y/N] ".format(player_name)).lower()

            players.append(player_name)
            num += 1

            self.clear_screen()
        return players

    # prompts the user for a series of inputs
    # returns a tuple: (input_string, orientation_string)
    # validation takes place outside
    def prompt_for_ship_placement(self, ship_to_place):
        print("Next ship: {}, Length: {}".format(
            ship_to_place.name, ship_to_place.length))

        done = False

        while not done:
            try:
                origin = self.get_cell_input(
                    "In what cell should we place the nose (e.g. F 2, A 7, etc...)? ")
            except ValueError as exc:
                print(exc)
                continue

            done = True

        while done:
            orientation = input(
                "Would you like it to be placed [H]orizontally or [V]ertically? ").strip().lower()
            try:
                validator.validate_orientation(orientation)
            except ValueError as exc:
                print(exc)
                continue

            done = False

        return (origin, orientation)

    # returns the tuple of the player's guess
    def prompt_for_guess(self):

        guessed = False

        while not guessed:
            try:
                guess = self.get_cell_input(
                    "What cell would you like to guess? ")
            except ValueError as ve:
                print(ve)
                continue

            guessed = True

        return guess

    # returns a tuple of the cell choice (e.g. (1,3), (10, 9))
    def get_cell_input(self, message):

        cell_choice_str = input(message).strip().lower()

        validator.validate_cell_choice(cell_choice_str, self.BOARD_SIZE)

        cell_list = cell_choice_str.split(" ")

        # cells are not zero-indexed
        column = ord(cell_list[0]) - ord('a') + 1

        return (column, int(cell_list[1]))

    def clear_screen(self):
        print("\033c", end="")

    def print_board_heading(self):
        print("   " + " ".join([chr(c)
                                for c in range(ord('A'), ord('A') + self.BOARD_SIZE)]))

    def print_board(self, board):
        self.print_board_heading()

        row_num = 1
        for row in board:
            print(str(row_num).rjust(2) + " " + (" ".join(row)))
            row_num += 1
        print()

    def construct_player_board(self, player, opponent, show_ships=True):

        board = []

        for row in range(1, self.BOARD_SIZE + 1):

            output_list = []

            for col in range(1, self.BOARD_SIZE + 1):

                icon = self.EMPTY

                if show_ships:
                    # printing player's own board
                    # show ships and opponent's hits and misses
                    for ship in player.ships:
                        if (col, row) in ship.cells.keys():
                            # hit, ship, or sunk
                            if ship.is_sunk():
                                icon = self.SUNK
                            elif (col, row) in opponent.hits:
                                icon = self.HIT
                            else:
                                # ship
                                if ship.is_horizontal:
                                    icon = self.HORIZONTAL_SHIP
                                else:
                                    icon = self.VERTICAL_SHIP
                        else:
                            # miss or empty
                            if (col, row) in opponent.misses:
                                icon = self.MISS

                else:
                    # printing opponent's board
                    # show player's hits and misses
                    for ship in opponent.ships:
                        if (col, row) in ship.cells.keys():
                            if ship.is_sunk():
                                icon = self.SUNK
                            elif (col, row) in player.hits:
                                icon = self.HIT
                        else:
                            if (col, row) in player.misses:
                                icon = self.MISS

                output_list.append(icon)

            board.append(output_list)

        return board

    def prompt_for_switch(self, opponent):

        while input("Now hand the computer to {}. Press [ENTER] when ready...".format(opponent)) != '':
            print("You should only press the [ENTER] key and nothing else!!!")
