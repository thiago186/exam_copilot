"""This file contains the parsers used to parse the messages from the user."""

import json

from utils.exceptions import ResponseParsingError

def json_parser(message: str):
    """
    Parse a string in format: json
    """
    message = message.replace("'", '"')
    try:
        parsed_message = json.loads(message)
        return parsed_message
    except json.JSONDecodeError:
        raise ResponseParsingError(f"Could not parse the response: {message}")
