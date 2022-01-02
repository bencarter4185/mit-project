"""
Test script to compare the magnetic fields calculated by the Biot-Savart solver vs. an analytical solution.

Circular loop
"""
# Internal Imports
from import_above import allow_above_imports
# External imports
from numpy import array, linspace
from scipy.constants import mu_0 as mu
import matplotlib.pyplot as plt


def main():
    """
    circular_loop_validation.py

    Parse `circular_loop_validation.json` for simulation properties

    Define a circular loop with properties:
        - centre (x, y, z) = (0, 0, 0)
        - radius = 2
        - number of points = 100
        - number of loops = 1
        - orientation (theta, phi) = (0, 0)
        - current (magnitude, phase) = (1A, 0)

    Calculate magnetic field for (x, y) = (0, 0) with z from 0.1m to 10m
    """
    # Internal imports
    from bs_wires import Wires
    from bs_solver import solve, b_abs
    from load_json import parse_json

    # Hard-code the json_path for sake of ease in this case
    json_path = "./modules/tests/validation_tests/params/circular_loop_validation.json"
    coils, actions = parse_json(json_path)

    # Create a new object Wires; a list of all wires and coils which have been created
    wires = Wires()
    for coil in coils:
        wires.new_wire(coil)

    # Hard coded to assume it needs to calculate magnetic field along a line.
    job = actions["calculate magnetic field"]
    xs = linspace(job["start point"]["x"], job["end point"]["x"], job["number of points"])
    ys = linspace(job["start point"]["y"], job["end point"]["y"], job["number of points"])
    zs = linspace(job["start point"]["z"], job["end point"]["z"], job["number of points"])
    points = array([xs, ys, zs])

    # Calculate resultant magnetic field via bs_solver
    b = solve(wires, points)
    b_mag = b_abs(b)

    # Extract wire properties for ease of analytical solution calculation
    test_loop = wires.wires[0]
    current = test_loop.current
    radius = test_loop.radius

    # Calculate analytical solution of magnetic field due to current loop
    b_analytical = abs(mu*current*radius**2/(2*(zs**2+radius**2)**(3.0/2.0)))

    # Plot graph of results
    plt.style.use("seaborn")
    _, ax = plt.subplots(ncols=1, nrows=1)

    ax.plot(zs, b_mag, label="Numerical solution")
    ax.scatter(zs, b_analytical, label="Analytical Solution")

    ax.legend()

    ax.set_xlabel(r"$z$ (m)")
    ax.set_ylabel(r"$B$ (T)")
    ax.set_title("Circular Loop Validation")

    plt.show()


if __name__ == "__main__":
    allow_above_imports()
    main()
