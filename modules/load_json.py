"""
Library file to load configuration JSON files.
"""
import json


def _evaluate_boolean(param):
    """
    Evaluates a parameter to a boolean True or False.

    Will throw an exception if the parameter is malformed.
    """
    # Define list of acceptable `True` and `False` values
    true_values = ["true", "t", "yes", "y"]
    false_values = ["false", "f", "no", "n"]

    # Evaluate whether either list contains true or false
    contains_true = any(ele in param for ele in true_values)
    contains_false = any(ele in param for ele in false_values)
    decision = [contains_true, contains_false]

    # Control flow to return boolean value or error out
    match decision:
        case [True, False]:
            return True
        case [False, True]:
            return False
        case _:
            raise Exception(f"Parameter {param} is malformed. Please supply a `True` or `False` value and try again.")


def parse_json(filepath):
    """
    Load the JSON file contents and print to screen.
    """
    # Load the JSON to a dictionary, `data`
    with open(filepath) as f:
        data = json.load(f)

    # Separate `coils` and `params` into their own dictionaries
    coils = data["coils"]
    actions = data["actions"]

    return coils, actions
