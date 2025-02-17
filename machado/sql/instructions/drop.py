from typing import Callable


def drop(
        table: tuple[str, Callable[[...], dict]],
        column: tuple[str, Callable[..., dict]] | None = None,
        cascade: bool = False
         ) -> str:
    metadata_function = table[1]
    metadata = metadata_function()

    name = metadata.get("name")
    schema = metadata.get("schema")

    if column:
        column_metadata = column[1]()
        column_name = column_metadata.get("name")
        return f"ALTER TABLE {f'{schema}.' if schema else ''}{name} DROP COLUMN {column_name}"

    return f"DROP TABLE {f'{schema}.' if schema else ''}{name} {'CASCADE' if cascade else ''}"