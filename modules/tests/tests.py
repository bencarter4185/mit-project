"""
Unit tests for my Biot-Savart code.

Currently only checks if my modules are importing correctly, but I may add more later
"""

# Boilerplate code for all Python tests in this directory to import the modules in the directory above
import unittest
import sys
from import_above import allow_above_imports
from numpy import all


class TestCalc(unittest.TestCase):
    def test_imports(self):
        # Import modules from the directory above
        # This should run without breaking
        # `noqa: F401` tells my linter to ignore that the modules are imported and unused
        from bs_solver import solve  # noqa: F401
        from bs_discretizer import discretize  # noqa: F401
        from bs_wires import Wire  # noqa: F401

        # Check all modules have imported without error
        conditions_to_pass = all([
            "bs_solver" in sys.modules,
            "bs_discretizer" in sys.modules,
            "bs_wires" in sys.modules,
        ])

        self.assertTrue(conditions_to_pass, "All modules loaded correctly")


if __name__ == "__main__":
    # Add importing from modules in the directory above
    allow_above_imports()

    # Run unit tests
    unittest.main()
