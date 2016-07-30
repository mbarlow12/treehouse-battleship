
from ship import Ship
import validator as validator


class Player(object):

    def __init__(self, name):
        self.name = name
        self.ships = []
        self.hits = []
        self.misses = []

    def ready(self, ship_number):

        return len(self.ships) == ship_number

    def add_ship(self, ship_to_add):
        if ship_to_add.name not in [ship.name for ship in self.ships]:
            self.ships.append(ship_to_add)
        else:
            raise Exception("That ship is already in the player's list.")

    def place_ship(self, ship, origin, orientation, board_size):
        try:
            validator.validate_ship_placement(
                origin, orientation, ship, self.ships, board_size)
        except ValueError as ve:
            raise ve

        column, row = origin

        ship_cells = []
        is_horizontal = True

        if orientation == 'h':
            ship_cells.extend([(col, row)
                               for col in range(column, column + ship.length)])
        elif orientation == 'v':
            ship_cells.extend([(column, r)
                               for r in range(row, row + ship.length)])
            is_horizontal = False

        ship.set_cells(ship_cells, is_horizontal)

    def make_guess(self, guess_tuple, opponent):

        try:
            validator.validate_guess(guess_tuple, self)
        except ValueError as ve:
            raise ve

        response = ""

        for ship in opponent.ships:
            if guess_tuple in ship.cells.keys():
                self.hits.append(guess_tuple)
                ship.cells[guess_tuple] = False

                if ship.is_sunk():
                    response = "You sank {}'s {}".format(
                        opponent.name, ship.name)
                return True, response

        self.misses.append(guess_tuple)
        return False, response
