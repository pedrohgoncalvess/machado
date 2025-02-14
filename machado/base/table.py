from string import Template
from typing import Callable


def table(
        name:str,
        *columns: str,
        schema: str | None = None,
        foreign_keys: list[Callable[[...], str] | str] | None = None,
        if_not_exists: bool = False
) -> str:

    base = Template(f"CREATE TABLE {'IF NOT EXISTS' if if_not_exists else ''} {schema + '.' if schema else ''}{name} ($columns)")

    return base.substitute(columns=", ".join(columns))

