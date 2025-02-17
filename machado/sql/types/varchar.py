def varchar(
        length: int = 50,
        fixed: bool = False
) -> str:
    """
    Generates a VARCHAR column definition for SQL.

    Parameters:
        length (int): Maximum length for VARCHAR
        fixed (bool): False for varchar, true for char

    Returns:
        str: Complete VARCHAR column definition

    Examples:
        >>> varchar("name")
        ' VARCHAR(50)'
    """
    if not fixed:
        return f"VARCHAR({length})"
    return f"CHAR({length})"
