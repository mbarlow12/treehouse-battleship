
def validate_cell_choice(input_string, board_size):

    columns = [chr(c) for c in range(ord('a'), (ord('a') + board_size))]

    input_list = input_string.split(" ")

    if len(input_list) != 2:
        raise ValueError(
            "Incorrect number of arguments. Please ensure there's a space between the row and column selection.")

    if input_list[0] not in columns:
        raise ValueError(
            "First argument must be a letter between A and {}.".format(columns[-1].upper()))

    try:
        if int(input_list[1]) not in range(1, board_size + 1):
            raise ValueError(
                "Second argument must be an integer between 1 and {}".format(board_size))
    except ValueError as ve:
        raise ValueError(
            "Second argument must be an integer between 1 and {}".format(board_size))


def validate_orientation(input_string):
    if input_string not in ['h', 'v']:
        raise ValueError(
            "Ships must be placed either [V]ertically or [H]orizontally.")

# check if the player has already guessed that cell
    # input has already been validated


def validate_guess(guess, player):
    made_guesses = set(player.hits + player.misses)
    if guess in made_guesses:
        raise ValueError("You've already guessed that cell. Try again.")


# ensure that a ship is placed fully on the board (i.e. doesn't hang off
# edge) and that it doesn't overlap with any other ships
def validate_ship_placement(origin, orientation, ship, ship_list, board_size):

    column, row = origin
    check = 0

    if orientation == 'h':

        check = column + ship.length - 1

        for col in range(column, column + ship.length):

            validate_ship_cell((col, row), ship, ship_list)

    elif orientation == 'v':

        check = row + ship.length - 1

        for r in range(row, row + ship.length):

            validate_ship_cell((column, r), ship, ship_list)

    if check > board_size:
        raise ValueError(
            "ERROR: Your {} must be placed fully on the board.".format(ship.name))


def validate_ship_cell(cell, ship, ship_list):
    for existing_ship in ship_list:
        if existing_ship.cells:
            if cell in existing_ship.cells.keys():
                raise ValueError("ERROR: Your {} overlaps with your {} at cell [{} {}]. Try again.".format(
                    ship.name, existing_ship.name, cell[0], cell[1]))
