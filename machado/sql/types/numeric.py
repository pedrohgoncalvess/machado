def numeric(
        precision: int = 10,
        scale: int = 3
) -> str:
    return f"NUMERIC({precision}, {scale})"