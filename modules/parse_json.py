"""
Library file to load configuration JSON files.
"""
import json
from numpy import array, sqrt, pi, deg2rad  # noqa: F401


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


def _parse_angle(angle, angle_unit=None):
    """
    Parse the angle, converting from degrees if requested.
    Assumes angle is given in radians unless otherwise stated.
    """
    match angle_unit:
        case ("degrees" | "deg" | "d"):
            return deg2rad(eval(angle))
        case _:
            return eval(angle)


def _parse_current(current):
    """
    Convert the phase into pythonic data type, combine into complex, then return
    """
    try:
        phase = _parse_angle(current["phase"], current["angle unit"])
    except KeyError:
        phase = _parse_angle(current["phase"])

    return complex(eval(current["modulus"]), phase)


def _parse_orientation(orientation):
    """
    Convert the angles into pythonic data types, combine into array, then return
    """
    try:
        theta = _parse_angle(orientation["theta"], orientation["angle unit"])
        phi = _parse_angle(orientation["phi"], orientation["angle unit"])
    except KeyError:
        theta = _parse_angle(orientation["theta"])
        phi = _parse_angle(orientation["phi"])

    return array([theta, phi])


def _parse_xyz(xyz):
    """
    Parse a point in 3D cartesian space (x, y, z).
    """
    return array([
        eval(xyz["x"]),
        eval(xyz["y"]),
        eval(xyz["z"])
        ])


def _parse_square(coil):
    """
    Parse square coil and convert into pythonic data types.
    """
    parsed_coil = {
        "name": coil["name"],
        "shape": coil["shape"],
        "centre": _parse_xyz(coil["centre"]),
        "length": eval(coil["side length"]),
        "dl": eval(coil["discretization length"]),
        "n": eval(coil["number of loops"]),
        "orientation": _parse_orientation(coil["orientation"]),
        "current": _parse_current(coil["current"])
    }

    return parsed_coil


def _parse_circle(coil):
    """
    Parse circular coil and convert into pythonic data types.
    """
    parsed_coil = {
        "name": coil["name"],
        "shape": coil["shape"],
        "centre": _parse_xyz(coil["centre"]),
        "radius": eval(coil["radius"]),
        "np": eval(coil["number of points"]),
        "n": eval(coil["number of loops"]),
        "orientation": _parse_orientation(coil["orientation"]),
        "current": _parse_current(coil["current"])
    }

    return parsed_coil


def _parse_coils(coils):
    """
    Iteratively parse all coils in JSON, converting into pythonic data types.
    """
    parsed_coils = []

    for coil in coils:
        # Work out what we're trying to parse
        match coil["shape"]:
            case "square":
                parsed_coil = _parse_square(coil)
            case "circle":
                parsed_coil = _parse_circle(coil)
            case _:
                shape = coil["shape"]
                raise Exception(f"ERROR: Code currently only supports circular and square current loops. You provided: \"{shape}\". Please specify either \"circle\" or \"square\".")  # noqa: E501

        parsed_coils.append(parsed_coil)

    return parsed_coils



def _parse_boolean(action, action_name):
    """
    Evaluates a parameter to a boolean True or False.
    Will throw an exception if the parameter is malformed.
    """
    # Return None if action[action_name] doesn't exist
    try:
        _ = action[action_name]
    except KeyError:
        return None

    # Define list of acceptable `True` and `False` values
    true_values = ["true", "t", "yes", "y"]
    false_values = ["false", "f", "no", "n"]

    # Evaluate whether either list contains true or false
    contains_true = any(ele in action[action_name].lower() for ele in true_values)
    contains_false = any(ele in action[action_name].lower() for ele in false_values)
    decision = [contains_true, contains_false]

    # Control flow to return boolean value or error out
    match decision:
        case [True, False]:
            return True
        case [False, True]:
            return False
        case _:
            raise Exception(f"Parameter {action[action_name]} is malformed. Please supply a `True` or `False` value and try again.")


def _parse_lim(action, action_name):
    """
    Parse xlim/ylim/zlim and convert to pythonic data types.
    If KeyError, return None.
    """
    try:
        return array([
            eval(action[action_name][0]),
            eval(action[action_name][1])
        ])
    except KeyError:
        return None


def _parse_plot(action):
    """
    Parse `plot coils` action and convert to pythonic data types.
    """
    parsed_action = {
        "name": action["name"],
        "execute": _parse_boolean(action, "execute"),
        "xlim": _parse_lim(action, "xlim"),
        "ylim": _parse_lim(action, "ylim"),
        "zlim": _parse_lim(action, "zlim"),
        "axes_equal": _parse_boolean(action, "axes equal")
    }

    return parsed_action


def _parse_slice_xy(action):
    parsed_action = {
        "name": action["name"],
        "execute": _parse_boolean(action, "execute"),
        "xlim": _parse_lim(action, "xlim"),
        "ylim": _parse_lim(action, "ylim"),
        "axes_equal": _parse_boolean(action, "axes equal"),
        "np": eval(action["number of points"])
    }

    return parsed_action


def _parse_validation(action):
    """
    Parse `validate magnetic field` action and convert to pythonic data types.
    """
    parsed_action = {
        "name": action["name"],
        "execute": _parse_boolean(action, "execute"),
        "shape": action["shape"],
        "start_point": _parse_xyz(action["start point"]),
        "end_point": _parse_xyz(action["end point"]),
        "np": eval(action["number of points"])
    }

    return parsed_action


def _parse_actions(actions):
    """
    Iteratively parse all actions in JSON, converting into pythonic data types.
    """
    parsed_actions = []

    for action in actions:
        # If action's execute parameter is set to false; skip
        if _parse_boolean(action, "execute") is False:
            continue

        # Work out what we're trying to parse
        match action["name"]:
            case "validate magnetic field":
                parsed_action = _parse_validation(action)
            case "plot coils":
                parsed_action = _parse_plot(action)
            case "plot slice xy":
                parsed_action = _parse_slice_xy(action)
     
        parsed_actions.append(parsed_action)

    return parsed_actions


def parse_json(filepath):
    """
    Load the JSON file contents and print to screen.
    """
    # Load the JSON to a dictionary, `data`
    with open(filepath) as f:
        data = json.load(f)

    # Separate `coils` and `actions` into their own dictionaries
    coils = data["coils"]
    actions = data["actions"]

    coils = _parse_coils(coils)
    actions = _parse_actions(actions)

    return coils, actions
