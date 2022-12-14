"""Define inverses."""


def get_negative(input_number: float) -> float:
    """Get additive inverse of a real number.

    Parameters
    ----------
    input_number : float
        value of number

    Returns
    -------
    float
        negative of ``input_number``

    Examples
    --------
    >>> from package_name_to_import_with.calculator_sub_package import get_negative
    >>> get_negative(1)
    -1
    >>> get_negative(-1)
    1
    """
    additive_inverse = (-1) * input_number

    return additive_inverse


def get_reciprocal(input_number: float) -> float:
    """Get multiplicative inverse of a real number.

    Parameters
    ----------
    input_number : float
        value of number

    Returns
    -------
    float
        reciprocal of ``input_number``

    Raises
    ------
    ValueError
        if ``input_number`` is zero

    Examples
    --------
    >>> from package_name_to_import_with.calculator_sub_package import get_reciprocal
    >>> get_reciprocal(2)
    0.5
    >>> get_reciprocal(0.5)
    2.0
    """
    try:
        multiplicative_inverse = 1 / input_number
    except ZeroDivisionError as error:
        raise ValueError("Multiplicative inverse is not defined for zero") from error
    else:
        return multiplicative_inverse
