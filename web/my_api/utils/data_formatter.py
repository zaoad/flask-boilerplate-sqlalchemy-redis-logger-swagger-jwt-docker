import hashlib
from typing import Any


def not_empty(value: Any) -> bool:
    """Tests if a value is not empty

    Args:
        value: an object to be tested

    Returns:
        Boolean value depending on whether the value was empty or not
    """
    if value is None:
        return False
    if len(value) == 0:
        return False
    return True


def get_sha1_hash(data: str) -> str:
    """Generates hex sha1 hash string from utf-8 string

    Args:
        data: String to be hashed

    Return:
        A hexadecimal string with sha1 hash of input string
    """
    return hashlib.sha1(data.encode("utf-8")).hexdigest()