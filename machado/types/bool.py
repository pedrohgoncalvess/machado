def boolean(
    default: bool | None = None,
) -> str:
    if default is not None:
        return f"BOOLEAN DEFAULT {default}"
    return "BOOLEAN"