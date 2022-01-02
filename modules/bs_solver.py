"""
Library file to solve the Biot-Savart law.
"""

from scipy.constants import mu_0 as mu
from numpy import array, zeros, complex_, sqrt, pi, cross
from itertools import pairwise
from bs_discretizer import discretize


def _magnitude(vec):
    """
    Returns the magnitude of a vector
    """
    return sqrt(vec.dot(vec))


def _solve_segment(segment, point, current):
    """
    Calculate the magnetic field for a small current element, at a given point.
    """
    # Generate an empty variable for the magnetic field
    db = zeros(3)

    # Calculate segment vector
    ux = segment[0][1] - segment[0][0]
    uy = segment[1][1] - segment[1][0]
    uz = segment[2][1] - segment[2][0]

    dl = array([ux, uy, uz])

    # Get reference point in the middle of the segment
    ux_r = (segment[0][1] + segment[0][0])/2
    uy_r = (segment[1][1] + segment[1][0])/2
    uz_r = (segment[2][1] + segment[2][0])/2

    rp = array([ux_r, uy_r, uz_r])

    # Displacement vector
    ux_d = point[0] - rp[0]
    uy_d = point[1] - rp[1]
    uz_d = point[2] - rp[2]

    r = array([ux_d, uy_d, uz_d])

    # Perform Biot-Savart integral calculation
    db = mu/(4*pi) * current * cross(dl, r) / _magnitude(r)**3

    return db


def _solve_without_discretization(wire, points):
    """
    Calculate the resultant magnetic field due to an arbitrary wire object, with no chunking.
    """

    # Store an `effective current`, which is the current in the wire where the real part is multiplied
    # by the number of turns, n
    current = complex(wire.current.real * wire.n, wire.current.imag)

    # Generate an empty variable for the magnetic field
    b = zeros((len(points[0]), 3), dtype=complex_)

    # Iterate through every segment of wire
    for ((x2, x1),
         (y2, y1),
         (z2, z1)) in zip(pairwise(wire.coordinates[0]),
                          pairwise(wire.coordinates[1]),
                          pairwise(wire.coordinates[2])):
        # Generate coordinates of resultant line segment
        segment = array([array([x1, x2]), array([y1, y2]), array([z1, z2])])

        # Iterate through every point in question and solve
        for j in range(len(points[0])):
            # Generate coordinates of point
            point = array([points[0][j], points[1][j], points[2][j]])
            b[j] += _solve_segment(segment, point, current)

    return b


def _solve_with_discretization(wire, points):
    """
    Calculate the resultant magnetic field due to an arbitrary wire object, for a given set of points.
    """

    # Store an `effective current`, which is the current in the wire where the real part is multiplied
    # by the number of turns, n
    current = complex(wire.current.real * wire.n, wire.current.imag)

    # Generate an empty variable for the magnetic field
    b = zeros((len(points[0]), 3), dtype=complex_)

    # Iterate through every segment of wire
    for ((x2, x1),
         (y2, y1),
         (z2, z1)) in zip(pairwise(wire.coordinates[0]),
                          pairwise(wire.coordinates[1]),
                          pairwise(wire.coordinates[2])):
        # Generate coordinates of resultant line segment
        segment = array([array([x1, x2]), array([y1, y2]), array([z1, z2])])

        # Discretize the segment into chunks
        segments = discretize(wire, segment, wire.dl)

        for ((dx2, dx1),
             (dy2, dy1),
             (dz2, dz1)) in zip(pairwise(segments[0]),
                                pairwise(segments[1]),
                                pairwise(segments[2])):
            segment_chunk = array([array([dx1, dx2]), array([dy1, dy2]), array([dz1, dz2])])
            # Iterate through every point in question and solve
            for j in range(len(points[0])):
                # Generate coordinates of point
                point = array([points[0][j], points[1][j], points[2][j]])
                b[j] += _solve_segment(segment_chunk, point, current)

    return b


def solve(wires, points):
    """
    Calculate the resultant magnetic field due to an arbitrary wire object, for a given set of points.

    Assume that if `dl` isn't supplied, no discretization is required.
    """
    # Generate an empty variable for the magnetic field
    b = zeros((len(points[0]), 3), dtype=complex_)

    for wire in wires.wires:
        match wire.shape:
            case "circle":
                b += _solve_without_discretization(wire, points)
            case "square":
                b += _solve_with_discretization(wire, points)

    return b


def b_abs(b):
    """
    Return the absolute value of a calculated magnetic field
    """
    b_abs = zeros(len(b))

    for i in range(len(b_abs)):
        b_abs[i] = abs(_magnitude(b[i]))

    return b_abs
