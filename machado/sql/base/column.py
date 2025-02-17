from typing import Callable


def column(
    name: str,
    data_type: Callable[..., str] | str,
    primary_key: bool = False,
    not_null: bool = False,
    unique: bool = False,
    default: any = None,
    extra_constraints: list[str] = None
) -> tuple[str, Callable[..., dict]]:
    """
    Base function to build column definitions with common parameters.
    """
    constraints = []

    data_type_f = data_type() if callable(data_type) else data_type

    base = f'''"{name}" {data_type_f}'''

    if primary_key:
        constraints.append("PRIMARY KEY")
    if unique:
        constraints.append("UNIQUE")
    if not_null:
        constraints.append("NOT NULL")
    if default is not None:
        constraints.append(f"DEFAULT {default}")
    if extra_constraints:
        constraints.extend(extra_constraints)

    def metadata():
        return {
            "name": name,
        }

    return " ".join([base] + constraints), metadata