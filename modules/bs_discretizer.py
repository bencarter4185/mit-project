"""
Library file to discretize wire elements.
"""

from numpy import array, floor, append, sqrt


def _magnitude(vec):
    """
    Returns the magnitude of a vector
    """
    return sqrt(vec.dot(vec))


def discretize(wire, segment, dl):
    """
    Discretize the nth segment of wire of chunk length dl
    """
    # Segment vector calculation
    ux = segment[0][1] - segment[0][0]
    uy = segment[1][1] - segment[1][0]
    uz = segment[2][1] - segment[2][0]

    u = array([ux, uy, uz])

    segment_len = _magnitude(u)

    # If segment is shorter than dl, return it
    if segment_len < dl:
        return segment

    # Calculate how many segments to make
    length_ratio = segment_len / dl
    n = floor(length_ratio)

    d_seg_x = array([segment[0][0]])
    d_seg_y = array([segment[1][0]])
    d_seg_z = array([segment[2][0]])

    # Calculate the length of the vector v
    v = dl*u / _magnitude(u)

    for i in range(1, int(n) + 1):
        d_seg_x = append(d_seg_x, d_seg_x[-1] + v[0])
        d_seg_y = append(d_seg_y, d_seg_y[-1] + v[1])
        d_seg_z = append(d_seg_z, d_seg_z[-1] + v[2])

    d_seg = array([d_seg_x, d_seg_y, d_seg_z])

    return d_seg
