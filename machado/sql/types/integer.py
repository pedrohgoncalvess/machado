INT_SIZES = {
    "big": "BIGINT",
    "small": "SMALLINT",
    "default": "INTEGER"
}

def integer(
    auto_increment: bool = False,
    size: str = "default",
) -> str:
    constraints = []
    if auto_increment:
        constraints.append("GENERATED ALWAYS AS IDENTITY")
    return f'''{INT_SIZES[size]} {" ".join(constraints)}'''