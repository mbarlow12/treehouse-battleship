
class Ship(object):
    """docstring for Ship"""

    def __init__(self, name, length):
        self.name = name
        self.length = length
        # cells is a dict of the ship's with tuples as keys
        # and booleans as values that will keep track of opponent hits
        self.cells = {}
        self.is_set = False

    def set_cells(self, cells, is_horizontal=True):
        # cells is a list of cells, loop over each and set each to true
        for cell in cells:
            self.cells[cell] = True

        self.is_horizontal = is_horizontal

        self.is_set = True

    def is_sunk(self):
        if True in self.cells.values():
            return False

        return True
