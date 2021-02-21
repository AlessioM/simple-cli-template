from pydantic import validate_arguments


@validate_arguments
def add_all(*numbers: int) -> int:
    """add numbers"""
    return sum(numbers)
