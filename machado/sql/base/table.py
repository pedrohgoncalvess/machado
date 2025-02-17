from string import Template
from typing import Callable


def table(
        name:str,
        *columns: tuple[str, Callable[..., dict]],
        schema: str | None = None,
        foreign_keys: list[Callable[[...], str] | str] | None = None,
        if_not_exists: bool = False
) -> tuple[str, Callable[..., dict]]:

    base = Template(f"CREATE TABLE {'IF NOT EXISTS' if if_not_exists else ''} {schema + '.' if schema else ''}{name} ($columns)")
    str_columns = [column[0] for column in columns]

    def metadata():
        return {
            "name": name,
            "columns": columns,
            "schema": schema
        }

    return base.substitute(columns=", ".join(str_columns)), metadata

