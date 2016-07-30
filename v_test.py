import validator as v
from ship import Ship

a = Ship("a", 1)
a.set_cells([(1,1)])

b = Ship("b", 2)
b.set_cells([(1,2), (2,2)])

c = Ship("c", 3)

v.validate_ship_placement((2,1), 'v', c, [a,b], 10)