"""
Test script to compare the magnetic fields calculated by the Biot-Savart solver vs. an analytical solution.

Circular loop
"""
# Internal Imports
from import_above import allow_above_imports
# External imports
from numpy import array, linspace, sqrt, sum, floor, log10
from scipy.constants import mu_0 as mu
import matplotlib.pyplot as plt
from timeit import timeit  # noqa: F401


def round_sig(x, sig=2):
    return round(x, sig-int(floor(log10(abs(x))))-1)


def main():
    """
    circular_loop_validation.py

    Parse `circular_loop_validation.json` for simulation properties
    """
    # Internal imports
    from bs_wires import Wires
    from parse_json import parse_json
    from bs_actions import do_action

    # Hard-code the json_path for sake of ease in this case
    json_path = "./modules/tests/validation_tests/params/circular_loop_validation.json"
    coils, actions = parse_json(json_path)

    # Create a new object Wires; a list of all wires and coils which have been created
    wires = Wires()
    for coil in coils:
        wires.new_wire(coil)

    # Iterate through all actions and perform them
    for action in actions:
        do_action(action, wires)


if __name__ == "__main__":
    allow_above_imports()
    main()
