"Get a json file and manipulate it"

import re
import json
from pathlib import Path
from typing import Dict


def get_json_with_placeholders(
    file_path: Path, values: Dict[str, str]
) -> Dict[str, str]:
    """Open a json file with variable placeholders and return a python dict
    with the real values in it.

    Args:
        file_path (Path): path where the json file is located
        values (dict): dictionary with the real value of each placeholder

    Returns:
        dict: python dictionary with the variables instead of the placeholders
    """
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read().replace("\n", "")
        content_replaced = replace_placeholders_in_string(content, values)
    return json.loads(content_replaced)


def replace_placeholders_in_string(
    string_data: str, values: Dict[str, str], character_for_sustitution: str = r"{}"
) -> str:
    """Find an replace all the variable placeholders in a string. By
    default, all the placeholders has to be between brackets like
    {my_var} but it can be changed.
    Based on https://gist.github.com/msguner/25dfb46bcd611858ce0ca5dc89d80a54

    Args:
        string_data (str): string with placeholders in it
        values (Dict[str, str]): dictionary with the real value of each placeholder
        character_for_sustitution (str, optional): character used in the string
            to enclose the variables. Defaults to r"{}".

    Raise:
        AssertionError: if any of the placeholders is not in the values dict

    Returns:
        str: string with the variables instead of the placeholders
    """

    # find all placeholders
    first_char = character_for_sustitution[0]
    second_char = character_for_sustitution[1]
    placeholders = set(
        re.findall(f"{first_char}[a-zA-Z0-9_ ]+{second_char}", string_data)
    )
    clear_placeholders = list(
        map(
            lambda x: x.replace(f"{first_char}", "").replace(f"{second_char}", ""),
            placeholders,
        )
    )

    assert all(
        item in values for item in clear_placeholders
    ), "Please enter the values of all placeholders."

    # replaces all placeholders with values
    for k, v in values.items():
        placeholder = f"{first_char}{k}{second_char}"
        string_data = string_data.replace(placeholder, v)

    return string_data
