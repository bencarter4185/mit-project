"""
Writing a biot-savart solver from scratch
"""

import matplotlib.pyplot as plt
from numpy import array, pi, zeros, linspace
import modules.bs_wires as bs_wires
import modules.bs_solver as bs_solver


def main():

    """
    Testing code to create an orientable square loop
    """

    # Square loop with current 2A, 0 phase, 20 loops
    some_loop = bs_wires.Wire()
    some_loop.square_loop(centre=array([0, 0, 0]), length=2, orientation=array([0*pi, 0]))
    some_loop.set_current(2, 0)
    some_loop.set_loops(20)

    zs = linspace(1, 10, 1000)
    xs = zeros(len(zs))
    ys = zeros(len(zs))

    points = array([xs, ys, zs])

    b = bs_solver.solve(some_loop, points, 0.01)
    b_mag = bs_solver.b_abs(b)

    b_no_chunk = bs_solver.solve_no_chunk(some_loop, points)
    b_mag_no_chunk = bs_solver.b_abs(b_no_chunk)

    plt.plot(zs, b_mag)
    plt.plot(zs, b_mag_no_chunk)
    plt.show()

    # # Square loop
    # square_loop = wires.Wire()
    # square_loop.square_loop(centre=array([0, 0, 0]), length=2, orientation=array([0, 0]))

    # print(square_loop.coordinates[0])

    # # Circular loop
    # circular_loop = wires.Wire()
    # circular_loop.circular_loop(centre=array([0, 0, 0]), radius=1, n_p=1000, n=1, orientation=array([0, 0]))

    # zs = range(1, 10)
    # xs = zeros(len(zs))
    # ys = zeros(len(zs))

    # points = array([xs, ys, zs])

    # b = solver.solve(circular_loop, points)

    # for i in range(len(square_loop.coordinates[0])):
    #     dx = square_loop.coordinates[0][i+1] - square_loop.coordinates[0][i]
    #     dy = square_loop.coordinates[1][i+1] - square_loop.coordinates[1][i]
    #     dz = square_loop.coordinates[2][i+1] - square_loop.coordinates[2][i]
    #     print([dx, dy, dz])

    # for ((x2, x1),
    #      (y2, y1),
    #      (z2, z1)) in zip(pairwise(square_loop.coordinates[0]),
    #                       pairwise(square_loop.coordinates[1]),
    #                       pairwise(square_loop.coordinates[2])):
    #     print(f"x1={x1}, x2={x2}, y1={y1}, y2={y2}, z1={z1}, z2={z2}")

    # x_pair = pairwise(square_loop.coordinates[0])

    # print(x_pair[0][0])

    # # Iterate through each (dx, dy, dz) == (x2 - x1, y2 - y1, z2 - z1)
    # for i in range(len(square_loop.coordinates[0]) - 1):
    #     print(i)

    # for x2, x1 in pairwise(square_loop.coordinates[0]):
    #     dx = x2 - x1
    #     print(dx)

    # print()
    # print(circular_loop.coordinates[0][0:20])

    # ax = some_loop.plotme()

    # some_loop_1 = wires.Wire()
    # some_loop_1.square_loop(centre=array([0, 0, 0]), length=1.5, orientation=array([pi/4, pi/3]))
    # some_loop_1.plotme(ax)

    # some_loop_2 = wires.Wire()
    # some_loop_2.square_loop(centre=array([0, 0, 0]), length=1.2, orientation=array([3*pi/2, pi/16]))
    # some_loop_2.plotme(ax)

    # some_loop_3 = wires.Wire()
    # some_loop_3.square_loop(centre=array([0, 0, 0]), length=0.75, orientation=array([pi/2, pi/2]))
    # some_loop_3.plotme(ax)

    # ax.axes.set_xlim3d(left=-1.2, right=1.2)
    # ax.axes.set_ylim3d(bottom=-1.2, top=1.2)
    # ax.axes.set_zlim3d(bottom=-1.2, top=1.2)

    # some_loop = wires.Wire()
    # some_loop.circular_loop(array([0, 0, 0]), 2, 100, 1, orientation= array([0, 0]))

    # ax = some_loop.plotme()

    # ax.axes.set_xlim3d(left=-2.2, right=2.2)
    # ax.axes.set_ylim3d(bottom=-2.2, top=2.2)
    # ax.axes.set_zlim3d(bottom=-2.2, top=2.2)

    # some_loop.circular_loop(array([0, 0, 0]), 1, 100, 1, orientation = array([0, pi/2]))
    # some_loop.plotme(ax)
    # some_loop.circular_loop(array([0, 0, 0]), 0.5, 100, 1, orientation = array([0, pi/4]))
    # some_loop.plotme(ax)
    # some_loop.circular_loop(array([0, 0, 0]), 2, 100, 1, orientation = array([0, 3*pi/4]))
    # some_loop.plotme(ax)

    # plt.show()


if __name__ == '__main__':
    main()
