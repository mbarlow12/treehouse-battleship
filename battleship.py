from game_display import Display
from player import Player
from ship import Ship


class Battleship(object):
    """Class to handle the mechanics of the battleship game (e.g. turn handling)
    and keep track of the endgame state.

    Variables:
        BOARD_SIZE {number} -- The size of the board (e.g. 10 -> 10 x 10 board)
        SHIP_INFO {list} -- A list of ship tuples to be used in the game
    """

    BOARD_SIZE = 10

    SHIP_INFO = [
        ("Aircraft Carrier", 5),
        ("Battleship", 4),
        ("Submarine", 3),
        ("Cruiser", 3),
        ("Dinghy", 2)
    ]

    def __init__(self):
        self.displayer = Display(self.BOARD_SIZE)
        players = self.displayer.prompt_for_names()
        self.player_1 = Player(players[0])
        self.player_2 = Player(players[1])

    def ready(self):
        """Checks that both the game's players have properly assigned their
        respective ships.

        Matches the length of each player's ship list to that of the initial
        SHIP_INFO of the game

        Returns:
            bool -- True if all lists are the same length.
        """
        return len(self.player_1.ships) == len(self.player_2.ships) == len(self.SHIP_INFO)

    def game_over(self):
        """Checks the end game state (all ships sunk) for both players.

        Returns:
            bool -- False if any ship for either player has an active cell.
        """
        for player in [self.player_1, self.player_2]:
            for ship in player.ships:
                if not ship.is_sunk():
                    return False

        return True

    def lost(self, player):
        """Checks whether a player's ships are all sunk.

        Arguments:
            player {Player} -- The player being checked.

        Returns:
            bool -- True only if all ships in the player's ships list are sunk.
        """

        for ship in player.ships:
            if not ship.is_sunk():
                return False

        return True

    def setup_game(self, player, opponent):
        """Prompts a single player to place their ships. Validates and finalizes
        ship placement.

        Arguments:
            player {Player} -- The participant placing ships
            opponent {Player} -- The placer's opponent (needed for board display)
        """

        self.displayer.clear_screen()

        ship_index = 0

        while not player.ready(len(self.SHIP_INFO)):
            # code to print the current board (starts empty)

            board = self.displayer.construct_player_board(
                player, opponent, True)
            self.displayer.print_board(board)

            ship_name, ship_length = self.SHIP_INFO[ship_index]
            ship_to_add = Ship(ship_name, ship_length)

            try:
                player.add_ship(ship_to_add)
            except Exception as e:
                ship_to_add = player.ships[ship_index]

            origin, orientation = self.displayer.prompt_for_ship_placement(
                ship_to_add)

            try:
                player.place_ship(ship_to_add, origin,
                                  orientation, self.BOARD_SIZE)
            except ValueError as ve:
                self.displayer.clear_screen()
                print(ve)
                print()
                continue

            self.displayer.clear_screen()
            ship_index += 1

        self.displayer.prompt_for_switch(opponent.name)

    def play_game(self):
        """Alternates player turns. Checks game status after each.

        Arguments:
            none

        Return:
            none

        Calls player_turn() on each player and checks the opponent's status
        after each. The loop is broken if either is determined to have lost.
        """

        player_1_turn = True

        while True:

            if player_1_turn:
                self.player_turn(self.player_1, self.player_2)

                if self.lost(self.player_2):
                    print("Game Over! You sank all {}'s ships!".format(
                        self.player_2.name))
                    break

                player_1_turn = False
            else:
                self.player_turn(self.player_2, self.player_1)

                if self.lost(self.player_1):
                    print("Game Over! You sank all {}'s ships!".format(
                        self.player_1.name))
                    break

                player_1_turn = True

    def player_turn(self, player, opponent):
        """Captures, validates, and runs a single player's guess against the
        given opponent.

        Arguments:
            player {Player} -- The participant making the guess
            opponent {Player} -- The target
        """

        self.displayer.clear_screen()

        guess_made = False

        while not guess_made:

            print("OPPONENT'S BOARD")
            board = self.displayer.construct_player_board(
                player, opponent, False)
            self.displayer.print_board(board)

            print("YOUR BOARD [{}]".format(player.name))
            board = self.displayer.construct_player_board(
                player, opponent, True)
            self.displayer.print_board(board)

            guess = self.displayer.prompt_for_guess()

            try:
                success, message = player.make_guess(guess, opponent)
            except Exception as ve:
                self.displayer.clear_screen()
                print(ve)
                print()
                continue

            guess_made = True

        if success:
            print("You got a hit!!!")
            if message != "":
                print(message)
        else:
            print("Bummer! You missed.")

        self.displayer.prompt_for_switch(opponent.name)


if __name__ == "__main__":

    the_game = Battleship()

    # while the game is not ready, prompt each player to set their ships

    while not the_game.ready():

        # loop over each player

            # while the player doesn't have all their ships set, loop over each
            # ship and prompt them for a starting cell and orientation

                # display current board of ships (empty to start)
                # prompt player for a ship placement
                # validate the ship placement (not off the edge and not
                # conflicting with other ships)

        the_game.setup_game(the_game.player_1, the_game.player_2)

        the_game.setup_game(the_game.player_2, the_game.player_1)

    #import pdb; pdb.set_trace()

    the_game.play_game()
