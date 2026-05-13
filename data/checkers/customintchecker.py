def check(answer: int) -> tuple[bool, str]:
    """Checks whether the answer lies between 50 and 100

    Args:
        answer (int): The answer to check

    Returns:
        tuple[bool, str]: Whether it's correct, and the feedback
    """
    if answer < 50:
        return (False, "Too low!")
    elif answer > 100:
        return (False, "Too high!")
    else:
        return (True, "Juuust right!")
