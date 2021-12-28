"""
Writing a biot-savart solver from scratch
"""

import matplotlib.pyplot as plt
from numpy import array, pi

import bs_wires as wires

def main():

    some_loop = wires.Wire()
    some_loop.square_loop(centre = array([0,0,0]), length = 1, orientation = array([0, pi/4]))

    ax = some_loop.plotme()

    print(some_loop.coordinates[0][0])

    ax.scatter(some_loop.coordinates[0][0], some_loop.coordinates[1][0], some_loop.coordinates[2][0])

    plt.show()

    # print(some_loop.coordinates)


    # # Create a new wire_element
    # wire = wires.Wire()

    # print(len(wire.coordinates))

    # # Add a new element from origin = (0, 0, 0)
    # wire.add_wire_element(0, 0, 5, origin=(0,0,0))
    # wire.add_wire_element(pi/2, 0, 2)

    # print(wire.coordinates)


if __name__ == '__main__':
    main()