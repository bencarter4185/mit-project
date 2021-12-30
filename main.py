"""
Writing a biot-savart solver from scratch
"""

import matplotlib.pyplot as plt
from numpy import array, pi

import wires

def main():

    """
    Testing code to create an orientable square loop
    """

    # some_loop = wires.Wire()
    # some_loop.square_loop(centre = array([0,0,0]), length = 2, orientation = array([pi/4, pi/3]))

    # ax = some_loop.plotme()

    # ax.axes.set_xlim3d(left=-1.2, right=1.2) 
    # ax.axes.set_ylim3d(bottom=-1.2, top=1.2) 
    # ax.axes.set_zlim3d(bottom=-1.2, top=1.2)

    # plt.show()

    some_loop = wires.Wire()
    some_loop.circular_loop(array([0, 0, 0]), 1, 100, 1, orientation = array([0, 0]))

    ax = some_loop.plotme()

    ax.axes.set_xlim3d(left=-2.2, right=2.2) 
    ax.axes.set_ylim3d(bottom=-2.2, top=2.2) 
    ax.axes.set_zlim3d(bottom=-2.2, top=2.2)

    some_loop.circular_loop(array([0, 0, 0]), 1, 100, 1, orientation = array([0, pi/2]))
    some_loop.plotme(ax)
    some_loop.circular_loop(array([0, 0, 0]), 0.5, 100, 1, orientation = array([0, pi/4]))
    some_loop.plotme(ax)
    some_loop.circular_loop(array([0, 0, 0]), 2, 100, 1, orientation = array([0, 3*pi/4]))
    some_loop.plotme(ax)

    plt.show()



if __name__ == '__main__':
    main()