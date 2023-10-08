"Test json_extras.load module"
from pathlib import Path
import pytest
from json_extras.load import replace_placeholders_in_string, get_json_with_placeholders

current_directory = Path(__file__).resolve().parent


def test_replace_placeholders_in_string():
    """Test that all the placeholders are replaced using
    replace_placeholders_in_string.
    """
    str_json_data = (
        r"{'first_key': 'the {first_value} and more', "
        r"'second_key': 'more than a {second_value}'}"
    )
    values = {"first_value": "real first value", "second_value": "real second value"}
    result = (
        r"{'first_key': 'the real first value and more', "
        r"'second_key': 'more than a real second value'}"
    )
    assert result == replace_placeholders_in_string(str_json_data, values)


def test_using_other_character():
    """Test if replace_placeholders_in_string works well with other character
    to enclose the variables.
    """
    string_data = r"This is a literal string <missing word> other type of character."
    values = {"missing word": "with"}
    result = r"This is a literal string with other type of character."
    assert result == replace_placeholders_in_string(string_data, values, "<>")


def test_missing_placeholder():
    """Test that raise an error when a placeholder is missing in the values
    dict.
    """
    str_json_data = (
        r"{'first_key': 'the {first value} and more', "
        r"'second_key': 'more than a {second value}'}"
    )
    values = {"first_value": "real first value"}
    with pytest.raises(AssertionError):
        replace_placeholders_in_string(str_json_data, values)


def test_more_variables_than_placeholders():
    """Test that has no problems with a values dict that has more than the
    needed variables.
    """
    str_json_data = (
        r"{'first_key': 'the {first_value} and more', "
        r"'second_key': 'more than a {second_value}'}"
    )
    values = {
        "first_value": "real first value",
        "second_value": "real second value",
        "third_value": "real third value",
    }
    result = (
        r"{'first_key': 'the real first value and more', "
        r"'second_key': 'more than a real second value'}"
    )
    assert result == replace_placeholders_in_string(str_json_data, values)


def test_repetead_placeholders():
    """Test replace_placeholders_in_string with a repeated placeholder. It must
    return the same value on each repetition.
    """
    str_json_data = (
        r"{'first_key': 'the {common_value} and more', "
        r"'second_key': 'more than a {common_value}', "
        r"'third_key': 'third value'}"
    )
    values = {"common_value": "real common value"}
    result = (
        r"{'first_key': 'the real common value and more', "
        r"'second_key': 'more than a real common value', "
        r"'third_key': 'third value'}"
    )
    assert result == replace_placeholders_in_string(str_json_data, values)


def test_get_json_with_placeholders():
    """Test that get_json_with_placeholders returns a dict with the
    placheholders replaced with the values passed.
    """
    file_path = current_directory / "test_load/json_with_placeholders.json"
    values = {
        "first_value": "real first value",
        "second_value": "real second value",
        "third_value": "real third value",
    }
    result = {
        "first_key": "The real first value and more",
        "second_key": "More than a real second value",
        "thir_key": "This has no placeholders",
    }
    assert result == get_json_with_placeholders(file_path, values)
