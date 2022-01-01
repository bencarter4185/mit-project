# Internal module imports
from modules.bs_discretizer import discretize
from modules.bs_wires import Wire
# External module imports
from numpy import array, pi

# Square loop with current 2A, 0 phase
some_loop = Wire()
# some_loop.square_loop(centre=array([0, 0, 0]), length=2, orientation=array([0*pi, 0]))
some_loop.circular_loop(centre=array([0, 0, 0]), radius=2, n_p=100, n=1, orientation=array([0*pi, 0]))
some_loop.set_current(2, 0)

ax = some_loop.plotme()

# Test the discretisation of the wire
d_segment = discretize(some_loop, 0.01, 1)

print(d_segment)
