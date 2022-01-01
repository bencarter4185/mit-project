"""
Test script to compare the magnetic fields calculated by the Biot-Savart solver vs. an analytical solution
"""
# Internal Imports
from import_above import allow_above_imports
# External imports
from numpy import array, linspace, zeros
from scipy.constants import mu_0 as mu
import matplotlib.pyplot as plt


def main():
    """
    Define a square loop with properties:
        - centre (x, y, z) = (0, 0, 0)
        - side length = 2
        - number of loops = 1
        - orientation (theta, phi) = (0, 0)
        - current (magnitude, phase) = (1A, 0)
    """
    # Internal imports
    from bs_wires import Wire
    from bs_solver import solve, b_abs, sqrt, pi

    # Define parameters of square loop
    centre = array([0, 0, 0])
    length = 2
    n = 1
    orientation = array([0, 0])
    current = complex(1, 0)

    # Define step length of discretized sections of wire
    dl = 0.01

    # Create loop
    test_loop = Wire()
    test_loop.square_loop(centre=centre, length=length, n=n, orientation=orientation, current=current)

    # Test the magnetic field of the current loop at (x, y) = (0, 0) and changing z
    zs = linspace(0.1, 10, 100)
    xs = zeros(len(zs))
    ys = zeros(len(zs))
    points = array([xs, ys, zs])

    # Calculate resultant magnetic field via bs-solver, with discretization
    b = solve(test_loop, points, dl)
    b_mag = b_abs(b)

    # Calculate resultant magnetic field via bs-solver, without discretization
    b_nd = solve(test_loop, points)
    b_nd_mag = b_abs(b_nd)

    # Calculate analytical solution of magnetic field due to current loop
    r = sqrt(zs**2 + (length/2)**2)
    b_analytical = abs((mu*test_loop.current)/(2*pi*r**2) * (length**2)/(sqrt(zs**2 + (length**2)/2)))

    # Plot graph of results
    plt.style.use("seaborn")
    _, ax = plt.subplots(ncols=1, nrows=1)

    ax.plot(zs, b_mag, label="Numerical solution with Discretization")
    ax.plot(zs, b_nd_mag, label="Numerical solution without Discretization")
    ax.scatter(zs, b_analytical, label="Analytical Solution")

    ax.legend()

    ax.set_xlabel(r"$z$ (m)")
    ax.set_ylabel(r"$B$ (T)")
    ax.set_title(f"Square Loop Validation, dl={dl}")

    plt.show()


if __name__ == "__main__":
    allow_above_imports()
    main()
